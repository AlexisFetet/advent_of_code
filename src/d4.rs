use std::fs;

use itertools::Itertools;
use regex::Regex;

#[derive(Debug)]
pub struct D4Solver {
    pub data: Vec<(String, u32, String)>,
}

impl D4Solver {
    pub fn extract_info(&mut self, input: String) {
        let re: Regex = Regex::new(r"(?<name>[a-z\-]+)-(?<sector>\d+)\[(?<order>[a-z]+)\]").unwrap();

        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        let instructions: Vec<(String, u32, String)> = re.captures_iter(&contents.as_str()).map(|captures| {
            let name: &str = captures.name("name").unwrap().as_str();
            let sector: &str = captures.name("sector").unwrap().as_str();
            let sector: u32 = sector.to_string().parse().unwrap();
            let order: &str = captures.name("order").unwrap().as_str();
            (name.to_string(), sector, order.to_string())
        }).collect();

        self.data = instructions;
    }

    pub fn solve_p1(&self) -> u32 {
        let mut result: u32 = 0;

        for (name, sector, order) in self.data.iter() {
            if f_is_real(name, order) {
                result += sector;
            }
        }

        result
    }

    pub fn solve_p2(&self) -> u32 {
        let mut result = 0;

        for (name, sector, order) in self.data.iter() {
            if f_is_real(name, order) {
                if f_do_caesar(name, *sector).contains("north") {
                    result = *sector;
                    break;
                }
            }
        }

        result
    }
}

fn f_is_real(name: &String, order: &String) -> bool {
    let filtered_name = &name.replace("-", "");
    let chars_in_name = filtered_name.chars().into_iter().unique();
    let mut actual_order: Vec<(usize, char)> = chars_in_name.map(|char_value|(name.matches(char_value).count(), char_value)).collect();
    actual_order.sort_by(|a, b| {
        if a.0 == b.0 { // same count
            return a.cmp(b) // compare letters alphabetically
        } else {
            return b.cmp(a) // reverse compare counts
        }
    });
    let actual_order_string = actual_order.into_iter().map(|f| f.1).collect::<String>();
    actual_order_string.starts_with(order)
}

fn f_do_caesar(input: &String, count: u32) -> String{

    let mut result = String::from("");

    for character in input.chars().into_iter() {
        result.push_str(&String::from(f_do_caesar_char(character, count)));
    }

    result

}

fn f_do_caesar_char(input: char, count: u32) -> char{
    if input == '-' {
        return ' '
    }
    char::from_u32(('a' as u32) + ((input as u32) - ('a' as u32) + count) % 26).expect("char invalide")
}

impl Default for D4Solver {
    fn default() -> D4Solver {
        D4Solver {data : vec![]}
    }
}