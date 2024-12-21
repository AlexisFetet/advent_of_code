use std::{collections::{HashMap, HashSet}, fs};

use itertools::Itertools;
use regex::Regex;

#[derive(Debug)]
pub struct D19Solver {
    pub patterns: HashSet<String>,
    pub designs: Vec<String>,
}

impl D19Solver {
    pub fn extract_info(&mut self, input: String) {
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");
        
        self.patterns.clear();
        self.designs.clear();
        let (patterns, designs) = contents.split("\n\n").collect_tuple().unwrap();
        for pattern in patterns.replace(',', "").split_ascii_whitespace().map(|string| String::from(string)) {
            self.patterns.insert(pattern);
        }
        self.designs = designs.lines().map(|string| String::from(string)).collect_vec();
    }

    pub fn solve_p1(&self) -> usize {
        let regex = Regex::new(["^(", self.patterns.iter().join("|").as_str(), ")+$"].concat().as_str()).unwrap();
        self.designs.iter().filter(|design| {
            regex.is_match(&design)
        }).count()
    }

    pub fn solve_p2(&self) -> u64 {
        self.designs.iter().map(|design| {
            count_match(&design, &self.patterns, &mut HashMap::<String, u64>::new())
        }).sum()
    }
}

impl Default for D19Solver {
    fn default() -> D19Solver {
        D19Solver {patterns : HashSet::<String>::new(), designs: vec![]}
    }
}

fn count_match(haystack: &str, patterns: &HashSet<String>, known: &mut HashMap<String, u64>) -> u64 {
    if known.contains_key(haystack) {
        return known[haystack];
    }
    if haystack.len() == 0 {
        return 1;
    }
    let mut matches = 0;
    for index in 1..=haystack.len() {
        if patterns.contains(haystack.get(..index).unwrap()) {
            let sub_result = count_match(&haystack[index..], patterns, known);
            known.insert(haystack[index..].to_string(), sub_result);
            matches += sub_result;
        }
    }
    matches
}
