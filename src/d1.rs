use std::{collections::HashMap, fs, vec};

use regex::Regex;

#[derive(Debug)]
pub struct D1Solver {
    pub data: Vec<Vec<i32>>,
}

impl D1Solver {
    pub fn extract_info(&mut self, input: String) {
        let re = Regex::new(r"(?<list1>\d+)\s*(?<list2>\d+)").expect("Regex should compile");

        // clear our container
        self.data.clear();
        self.data.push(vec![]);
        self.data.push(vec![]);

        // get file content
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        // process data
        for line in contents.lines() {
            let match_in_line = re.captures(line).unwrap();
            self.data[0].push(match_in_line.name("list1").expect("").as_str().parse().unwrap());
            self.data[1].push(match_in_line.name("list2").expect("").as_str().parse().unwrap());
        }
        self.data[0].sort(); // we can use sorted lists for both parts
        self.data[1].sort(); // we can use sorted lists for both parts

    }

    pub fn solve_p1(&self) -> i32 {
        let mut result = 0;
        // the lists are sorted so just add the delta for the result
        for indx in 0..self.data[0].len() {
            result += (self.data[0][indx] - self.data[1][indx]).abs();
        }
        result
    }

    pub fn solve_p2(&self) -> i32 {
        let mut integer_count_1 = count_integers(&self.data[1]);

        let mut result = 0;
        for int in self.data[0].iter() { 
            result += (*int) * (*integer_count_1.entry(*int).or_insert(0));
        }
        result
    }
}

fn count_integers(data: &Vec<i32>) -> HashMap::<i32, i32> {
    let mut integer_count = HashMap::new();
    for int in data.iter() {
        *integer_count.entry(*int).or_insert(0) += 1;
    }
    integer_count
}

impl Default for D1Solver {
    fn default() -> D1Solver {
        D1Solver {data : vec![]}
    }
}