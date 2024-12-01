use std::collections::hash_map;
use std::fs;
use std::iter;

#[derive(Debug)]
pub struct D6Solver {
    pub data: Vec<String>,
}

impl D6Solver {
    pub fn extract_info(&mut self, input: String) {
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");
        
        self.data.clear();
        for line in contents.lines() {
            if self.data.is_empty() {
                self.data = iter::repeat(String::from("")).take(line.len()).collect();
            }
            for (index, character) in line.char_indices() {
                self.data[index].push(character);
            }
        }
    }

    pub fn solve_p1(&self) -> String {
        let mut result = String::from("");
        for column in self.data.iter() {
            let mut triage: hash_map::HashMap<char, u32> = hash_map::HashMap::new();
            for character in column.chars() {
                if triage.contains_key(&character) {
                    triage.insert(character, triage[&character] + 1);
                } else {
                    triage.insert(character,  1);
                }
            }
            let mut m: char = ' ';
            let mut current_max: u32 = 0;
            for (current_character, count) in triage {
                if count > current_max {
                    current_max = count;
                    m = current_character;
                }
            }
            result.push(m);
        }
        result
    }

    pub fn solve_p2(&self) -> String {
        let mut result = String::from("");
        for column in self.data.iter() {
            let mut triage: hash_map::HashMap<char, u32> = hash_map::HashMap::new();
            for character in column.chars() {
                if triage.contains_key(&character) {
                    triage.insert(character, triage[&character] + 1);
                } else {
                    triage.insert(character,  1);
                }
            }
            let mut m: char = ' ';
            let mut current_min: u32 = 0xFFFF;
            for (current_character, count) in triage {
                if count < current_min {
                    current_min = count;
                    m = current_character;
                }
            }
            result.push(m);
        }
        result
    }
}

impl Default for D6Solver {
    fn default() -> D6Solver {
        D6Solver {data : vec![]}
    }
}