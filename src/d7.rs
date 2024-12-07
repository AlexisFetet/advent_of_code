use std::{collections::VecDeque, fs};

use regex::{self, Regex};

#[derive(Debug)]
pub struct D7Solver {
    pub data: Vec<(i64, VecDeque<i64>)>,
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
        let mut result = 0;
        for (operation_result, operands) in self.data.iter() {
            if check(&mut operands.clone(), *operation_result, 1) {
                result += operation_result;
            }
        }
        result
    }

    pub fn solve_p2(&self) -> i64 {
        let mut result = 0;
        for (operation_result, operands) in self.data.iter() {
            if check(&mut operands.clone(), *operation_result, 2) {
                result += operation_result;
            }
        }
        result
    }
}

impl Default for D7Solver {
    fn default() -> D7Solver {
        D7Solver {data : vec![]}
    }
}

fn check(numbers: &mut VecDeque<i64>, target: i64, part: i32) -> bool {
    if target < 0 {return false;}
    if numbers.len() == 1 {
        return *(numbers.back().unwrap()) == target;
    }
    let tail = numbers.pop_back().unwrap();
    let mut result = false;
    if (target % tail) == 0 {
        result |= check(&mut numbers.clone(), target / tail, part);
    }
    if part == 2 {
        if target.to_string().ends_with(&tail.to_string()) && (target != tail) {
            result |= check(&mut numbers.clone(), target.to_string().strip_suffix(&tail.to_string()).unwrap().parse::<i64>().unwrap(), part);
        }
    }
    result |= check(numbers, target - tail, part);
    result
}
