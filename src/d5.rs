use std::{fs, usize};

use md5;

#[derive(Debug)]
pub struct D5Solver {
    pub data: String,
}

impl D5Solver {
    pub fn extract_info(&mut self, input: String) {
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.data = contents;
    }

    pub fn solve_p1(&self) -> String {
        let mut result = String::from("");
        let mut counter = 0;
        let data =  self.data.clone();

        while result.len() < 8 {
            let digest = md5::compute(format!("{data}{counter}"));
            let repr = String::from(format!("{:x}", digest));
            if repr.starts_with("00000") {
                result.push(repr.chars().nth(5).expect(""));
            }
            counter += 1;
        }

        result
    }

    pub fn solve_p2(&self) -> String {
        let mut result = String::from("........");
        let mut counter = 0;
        let data =  self.data.clone();

        while result.contains(".") {
            let digest = md5::compute(format!("{data}{counter}"));
            let repr = String::from(format!("{:x}", digest));
            if repr.starts_with("00000") {
                let indx: usize = match repr.chars().nth(5).expect("").to_string().parse() {
                    Ok(integer) => integer,
                    Err(_error) => {
                        counter += 1;
                        continue;
                    },
                };
                if indx < 8 {
                    if &result.chars().nth(indx).expect("").to_string() == "." {
                        result.replace_range(indx..indx+1, &repr.chars().nth(6).expect("").to_string());
                    }
                }
            }
            counter += 1;
        }

        result
    }
}

impl Default for D5Solver {
    fn default() -> D5Solver {
        D5Solver {data : String::from("")}
    }
}