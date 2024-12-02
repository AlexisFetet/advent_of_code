use std::{fs, iter::zip};

#[derive(Debug)]
pub struct D2Solver {
    pub data: Vec<Vec<i32>>,
}

impl D2Solver {
    pub fn extract_info(&mut self, input: String) {
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.data.clear();
        self.data = contents.lines().map(|line| {
            line.split_whitespace().map(|number| number.parse().unwrap()).collect()
        }).collect();
    }

    pub fn solve_p1(&self) -> u32 {
        let mut result = 0;
        for line in self.data.iter() {
            if is_valid_sequence(line) {
                result += 1;
            }
        }
        result
    }

    pub fn solve_p2(&self) -> u32 {
        let mut result = 0;
        for line in self.data.iter() {
            let mut is_valid = true;
            let sign = (line[0] - line[1]).signum();

            for indx in 0..line.len()-2 {
                let (value1, value2, value3) = (line[indx], line[indx + 1], line[indx + 2]);
                let is_12_ok = (1 <= (value1 - value2).abs()) && ((value1 - value2).abs() <= 3 ) && ((value1 - value2).signum() == sign);
                let is_23_ok = (1 <= (value2 - value3).abs()) && ((value2 - value3).abs() <= 3 ) && ((value2 - value3).signum() == sign);

                if is_12_ok && is_23_ok {
                    // so far so good
                    continue;
                } else {
                    is_valid = false; // need a subsequence that is valid
                }
                // trying with either 3 values removed
                for delta in 0..3 {
                    let mut data = line[..(indx + delta)].to_vec();
                    data.append(&mut line[(indx + 1 + delta)..].to_vec());
                    is_valid |= is_valid_sequence(&data);
                    if is_valid {break;}
                }
                break;
            }

            if is_valid {
                result += 1;
            }
        }
        result
    }
}

fn is_valid_sequence(data: &Vec<i32>) -> bool {
    let mut is_valid = true;
    let sign = (data[0] - data[1]).signum();
    for (value1, value2) in zip(data[..(data.len() - 1)].iter(), data[1..].iter()) {
        let is_12_ok = (1<= (value1 - value2).abs()) && ((value1 - value2).abs() <= 3 ) && ((value1 - value2).signum() == sign);
        if !is_12_ok {
            is_valid = false;
            break;
        }
    }
    is_valid
}

impl Default for D2Solver {
    fn default() -> D2Solver {
        D2Solver {data : vec![]}
    }
}