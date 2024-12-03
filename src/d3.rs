use std::fs;

use regex::{self, Regex};

#[derive(Debug)]
pub struct D3Solver {
    pub data: String,
}

impl D3Solver {
    pub fn extract_info(&mut self, input: String) {
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");
        self.data = contents; 
    }

    pub fn solve_p1(&self) -> i32 {
        let re = Regex::new(r"mul\((?<d1>[0-9]{1,3}),(?<d2>[0-9]{1,3})\)").expect("");
        re.captures_iter(&self.data).map(|captures| {
            captures.name("d1").unwrap().as_str().parse::<i32>().unwrap() * captures.name("d2").unwrap().as_str().parse::<i32>().unwrap()
        }).fold(0, |acc, x| acc + x)
    }

    pub fn solve_p2(&self) -> i32 {
        let mut enabled = true;
        let re = Regex::new(r"(?<do>do\(\))|(?<dont>don't\(\))|mul\((?<d1>[0-9]{1,3}),(?<d2>[0-9]{1,3})\)").expect("");
        re.captures_iter(&self.data).map(|captures| {
            let mut result = 0;
            if captures.name("dont").is_some() {
                enabled = false
            }
            if captures.name("do").is_some() {
                enabled = true
            }
            result += captures.name("d1").map_or(0, |f| {
                let temp = f.as_str().parse::<i32>().unwrap() * captures.name("d2").unwrap().as_str().parse::<i32>().unwrap();
                if enabled {return temp;} else {return 0;}
            });
            result
            
        }).fold(0, |acc, x| acc + x)
    }
}

impl Default for D3Solver {
    fn default() -> D3Solver {
        D3Solver {data : String::from("")}
    }
}