use std::fs;

use regex::Regex;

#[derive(Debug)]
pub struct D7Solver {
    pub data: Vec<String>,
}

impl D7Solver {
    pub fn extract_info(&mut self, input: String) {

        let contents = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.data = contents.lines().map(|f| String::from(f)).collect();
    }

    pub fn solve_p1(&self) -> u32 {
        let mut result = 0;
        let re_cleanser = Regex::new(r"\[(?<chars>[a-z]+)\]").unwrap();
        

        'external: for line in self.data.iter() {
            let mut is_valid = false;
            // check inside the brackets
            for extract in re_cleanser.captures_iter(&line) {
                let data = String::from(extract.name("chars").expect("").as_str());
                if data.len() >= 4 {
                    for indx in 0..(data.len() - 3) {
                        if is_palyndrome_4(&data[indx..indx+4]) {
                            continue 'external;
                        }
                    }
                }
            }
            let cleaned_line = re_cleanser.replace_all(line, "\n");
            // check outside the brackets
            'internal: for scrap in cleaned_line.lines() {
                let scrap = String::from(scrap);
                if scrap.len() >= 4 {
                    for indx in 0..(scrap.len() - 3) {
                        if is_palyndrome_4(&scrap[indx..indx+4]) {
                            is_valid = true;
                            break 'internal;
                        }
                    }
                }
            }
            if is_valid {
                result += 1;
            }
        }
        result
    }

    pub fn solve_p2(&self) -> u32 {
        let mut result = 0;
        let re_cleanser = Regex::new(r"\[(?<chars>[a-z]+)\]").unwrap();
        

        for line in self.data.iter() {
            let mut is_valid = false;
            let cleaned_line = re_cleanser.replace_all(line, "\n");
            let mut pals = vec![];
            // check outside the brackets for all 3 palyndromes
            for scrap in cleaned_line.lines() {
                let scrap = String::from(scrap);
                if scrap.len() >= 3 {
                    for indx in 0..(scrap.len() - 2) {
                        let pal = is_palyndrome_3(&scrap[indx..indx+3]);
                        if pal.len() > 0 {
                            pals.push(pal);
                        }
                    }
                }
            }
            // check inside the brackets
            'internal: for extract in re_cleanser.captures_iter(&line) {
                let data = String::from(extract.name("chars").expect("").as_str());
                for pal in pals.iter() {
                    if data.contains(pal) {
                        is_valid = true;
                        break 'internal;
                    }
                }
            }
            if is_valid {
                result += 1;
            }
        }
        result
    }
}

fn is_palyndrome_4(data: &str) -> bool {
    let mut is_valid = false;
    if (&data[0..1] == &data[3..4]) && (&data[1..2] == &data[2..3]) && (&data[0..1] != &data[1..2]) {
        is_valid = true;
    }
    is_valid
}

fn is_palyndrome_3(data: &str) -> String {
    let mut result = String::from("");
    if (&data[0..1] == &data[2..3]) && (&data[0..1] != &data[1..2]) {
        let char1 = &data[0..1];
        let char2 = &data[1..2];
        result = String::from(format!("{char2}{char1}{char2}"));
    }
    result
}

impl Default for D7Solver {
    fn default() -> D7Solver {
        D7Solver {data : vec![]}
    }
}