use std::fs;

use regex::{self, Regex};

#[derive(Debug)]
pub struct D7Solver {
    pub data: Vec<(i64, Vec<i64>)>,
}

impl D7Solver {
    pub fn extract_info(&mut self, input: String) {
        let re = Regex::new(r"(?<result>\d+):(?<operands>(?: \d+)+)").unwrap();
        let re_num = Regex::new(r" (?<num>\d+)").unwrap();

        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.data.clear();
        self.data = re.captures_iter(&contents).map(| capture | {
            (capture.name("result").unwrap().as_str().parse::<i64>().unwrap(), re_num.captures_iter(capture.name("operands").unwrap().as_str()).map(| inner_capture | {
                inner_capture.name("num").unwrap().as_str().parse::<i64>().unwrap()
            }).collect())
        }).collect();
    }

    pub fn solve_p1(&self) -> i64 {
        self.data.iter().filter(| (operation_result, operands) |
            check(&operands[..], *operation_result, 1)
        ).fold(0, | acc, (operation_result, _operands) |
            acc + operation_result
        )
    }

    pub fn solve_p2(&self) -> i64 {
        self.data.iter().filter(| (operation_result, operands) |
            check(&operands[..], *operation_result, 2)
        ).fold(0, | acc, (operation_result, _operands) |
            acc + operation_result
        )
    }
}

impl Default for D7Solver {
    fn default() -> D7Solver {
        D7Solver {data : vec![]}
    }
}

fn check(numbers: &[i64], target: i64, part: i32) -> bool {
    if target < 0 {return false;}
    if numbers.len() == 1 {
        return numbers[0] == target;
    }
    let tail = numbers[numbers.len() - 1];
    let mut result = false;
    if (target % tail) == 0 {
        result |= check(&numbers[..(numbers.len() - 1)], target / tail, part);
    }
    if part == 2 {
        if target.to_string().ends_with(&tail.to_string()) && (target != tail) {
            result |= check(&numbers[..(numbers.len() - 1)], target.to_string().strip_suffix(&tail.to_string()).unwrap().parse::<i64>().unwrap(), part);
        }
    }
    result |= check(&numbers[..(numbers.len() - 1)], target - tail, part);
    result
}
