use std::{collections::HashMap, fs};

#[derive(Debug)]
pub struct D11Solver {
    pub data: HashMap<i64, i64>,
}

impl D11Solver {
    pub fn extract_info(&mut self, input: String) {
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.data.clear();

        for number in contents.split_ascii_whitespace().into_iter() {
            self.data.entry(number.parse().unwrap()).or_insert(1);
        }
    }

    pub fn solve_p1(&self) -> i64 {
        loop_stones_process(self.data.clone(), 25)
    }

    pub fn solve_p2(&self) -> i64 {
        loop_stones_process(self.data.clone(), 75)
    }
}

impl Default for D11Solver {
    fn default() -> D11Solver {
        D11Solver {data : HashMap::new()}
    }
}

fn process_stone(stone_value: i64) -> (i64, Option<i64>) {
    let digit_count = (stone_value as f32).log10() as u32 + 1;
    if stone_value == 0 {
        return (1, None);
    } else if digit_count % 2 == 0 {
        let power_10 = (10 as i64).pow(digit_count / 2);
        return (stone_value / power_10, Some(stone_value % power_10))
    } else {
        return (stone_value * 2024, None);
    }
}

fn loop_stones_process(mut stones: HashMap<i64, i64>, loops: i64) -> i64 {
    for _ in 0..loops {
        let mut tmp = HashMap::new();
        for (key, value) in stones.iter() {
            let (stone1, maybe_stone2) = process_stone(*key);
            *tmp.entry(stone1).or_insert(0) += value;
            match maybe_stone2 {
                Some(stone2) => *tmp.entry(stone2).or_insert(0) += value,
                None => {}
            }
        }
        stones = tmp;
    }
    stones.values().fold(0, | acc, stone_count | acc + stone_count)
}
