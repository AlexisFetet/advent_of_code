use std::{collections::{HashMap, HashSet, VecDeque}, fs};

use itertools::Itertools;

#[derive(Debug)]
pub struct D22Solver {
    pub final_secret_numbers: Vec<u64>,
    pub sequences_gains: HashMap<VecDeque<i64>, u64>
}

impl D22Solver {
    pub fn extract_info(&mut self, input: String) {
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        // compute everything we need once
        self.final_secret_numbers.clear();
        self.sequences_gains.clear();

        let mut known = HashMap::<u64, u64>::new();
        let data = contents.lines().map(|value| value.parse::<u64>().unwrap()).collect_vec();
        for index in 0..data.len() {
            let mut secret_number = data[index];
            let mut old_price = secret_number % 10;
            let mut sequence: VecDeque<i64> = VecDeque::with_capacity(4);
            let mut known_sequences: HashSet<VecDeque<i64>> = HashSet::new();
            for _ in 0..2000 {
                secret_number = *known.entry(secret_number).or_insert(process_once(secret_number));
                let new_price = secret_number % 10;
                let delta = (new_price - old_price) as i64;
                if sequence.len() == 4 {sequence.pop_front();}
                sequence.push_back(delta);
                old_price = new_price;
                if !known_sequences.contains(&sequence) {
                    known_sequences.insert(sequence.clone());
                    *self.sequences_gains.entry(sequence.clone()).or_insert(0) += new_price;
                }
            }
            self.final_secret_numbers.push(secret_number);
        }
    }

    pub fn solve_p1(&self) -> u64 {
        self.final_secret_numbers.iter().sum()
    }

    pub fn solve_p2(&self) -> u64 {
        *self.sequences_gains.values().max().unwrap()
    }
}

impl Default for D22Solver {
    fn default() -> D22Solver {
        D22Solver {final_secret_numbers : vec![], sequences_gains: HashMap::<VecDeque<i64>, u64>::default()}
    }
}

fn process_once(input: u64) -> u64 {
    let tmp = input << 6;
    let tmp = input ^ tmp;
    let input_after_step_1 = tmp & (16777215);
    let tmp = input_after_step_1 >> 5;
    let tmp = input_after_step_1 ^ tmp;
    let input_after_step_2 = tmp & (16777215);
    let tmp = input_after_step_2 << 11;
    let tmp = input_after_step_2 ^ tmp;
    let input_after_step_3 = tmp & (16777215);
    input_after_step_3
}

