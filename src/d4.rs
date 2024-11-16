use std::fs;

use regex::Regex;

#[derive(Debug)]
pub struct D4Solver {
    pub data: Vec<(String, i32, String)>,
}

impl D4Solver {
    pub fn extract_info(&mut self, input: String) {
        let re: Regex = Regex::new(r"(?<name>[a-z\-]+)-(?<sector>\d+)\[(?<order>[a-z]+)\]").unwrap();

        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        let instructions: Vec<(String, i32, String)> = re.captures_iter(&contents.as_str()).map(|captures| {
            let name: &str = captures.name("name").unwrap().as_str();
            let sector: &str = captures.name("sector").unwrap().as_str();
            let sector: i32 = sector.to_string().parse().unwrap();
            let order: &str = captures.name("order").unwrap().as_str();
            (name.to_string(), sector, order.to_string())
        }).collect();

        self.data = instructions;
    }

    pub fn solve_p1(&self) -> u32 {
        0
    }

    pub fn solve_p2(&self) -> u32 {
        0
    }
}

impl Default for D4Solver {
    fn default() -> D4Solver {
        D4Solver {data : vec![]}
    }
}