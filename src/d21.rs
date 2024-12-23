use std::{collections::HashMap, fs};

use itertools::Itertools;
use regex::Regex;

#[derive(Debug)]
pub struct D21Solver {
    pub data: HashMap<String, u64>
}

fn get_next_digit(digit: char) -> u64 {
    match digit {
        'A' => 2,
        '0' => 1,
        value => value.to_digit(10).unwrap() as u64 + 2
    }
}

fn generate_sequence_for_next_dir(current: u64, next: u64, forbidden: i32) -> Vec<Vec<u64>> {
    let (delta_x, delta_y) = ((next % 3 - current % 3) as i32, (next / 3 - current / 3) as i32);
    let mut result = vec![];
    for vert_first in 0..2 {
        if vert_first == 1 && (current as i32 + delta_y * 3 != forbidden) {
            let mut sub_result = vec![];
            for _ in 0..delta_y.abs() {
                sub_result.push(1 + (3 * (1 + delta_y.signum())) as u64 / 2);
            }
            for _ in 0..delta_x.abs() {
                sub_result.push((1 + delta_x.signum()) as u64);
            }
            sub_result.push(5);
            result.push(sub_result);
        } else if current as i32 + delta_x != forbidden {
            let mut sub_result = vec![];
            for _ in 0..delta_x.abs() {
                sub_result.push((1 + delta_x.signum()) as u64);
            }
            for _ in 0..delta_y.abs() {
                sub_result.push(1 + (3 * (1 + delta_y.signum())) as u64 / 2);
            }
            sub_result.push(5);
            result.push(sub_result);
        }
    }
    result.iter().dedup().map(|elem|elem.clone()).collect_vec()
}

impl D21Solver {
    pub fn extract_info(&mut self, input: String) {
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        let re = Regex::new(r"\d+").unwrap();

        self.data.clear();
        for code in contents.lines() {
            self.data.insert(code.to_string(), re.captures(code).unwrap().get(0).unwrap().as_str().parse::<u64>().expect(""));
        }
    }

    pub fn solve_p1(&self) -> u64 {
        solve_for_n_robots(2, self.data.clone())
    }

    pub fn solve_p2(&self) -> u64 {
        solve_for_n_robots(25, self.data.clone())
    }
}

impl Default for D21Solver {
    fn default() -> D21Solver {
        D21Solver {data : HashMap::<String, u64>::new()}
    }
}

fn mix(possibilities: Vec<Vec<Vec<u64>>>) -> Vec<Vec<u64>> {
    let mut candidates: Vec<Vec<u64>> = possibilities[0].clone();
    for moves in possibilities[1..].iter() {
        let init_len = candidates.len();
        for _ in 1..moves.len() {
            candidates.append(&mut candidates.clone());
        }
        assert!(candidates.len() == init_len * moves.len());
        for (index, movements) in candidates.iter_mut().enumerate() {
            movements.append(&mut moves[index / init_len].clone());
        }
    }
    candidates
}

fn prune(possibilities: Vec<Vec<u64>>) -> Vec<Vec<u64>> {
    let min_len = possibilities.iter().map(|elem|elem.len()).min().unwrap();
    possibilities.iter().filter(|elem|elem.len() == min_len).map(|elem| elem.clone()).unique().collect_vec()
}

fn build_movements() -> HashMap<(u64, u64), Vec<u64>> {
    let mut result = HashMap::<(u64, u64), Vec<u64>>::new();
    for start in 0..=5 {
        if start == 3 {continue;}
        for end in 0..=5 {
            if end == 3 {continue;}
            let requested_moves = vec![vec![end]];

            let requested_moves_after1 = requested_moves.iter().map(|moves| {
                let mut current = start;
                let possibilities = moves.iter().map(|next| {
                    let sequences = generate_sequence_for_next_dir(current, *next, 3);
                    current = *next;
                    sequences
                }).collect_vec();
                mix(possibilities)
            }).concat();

            if requested_moves_after1.len() == 1 {
                result.insert((start, end), requested_moves_after1[0].clone());
                continue;
            }

            let mut reverse_1_2 = HashMap::<Vec<u64>, Vec<u64>>::new();
            let mut requested_moves_after2 = vec![];
            
            for possibility in requested_moves_after1.iter() {
                let mut current = 5;
                let possibilities = possibility.iter().map(|next| {
                    let sequences = generate_sequence_for_next_dir(current, *next, 3);
                    current = *next;
                    sequences
                }).collect_vec();
                let possibilities = mix(possibilities);
                requested_moves_after2.append(&mut possibilities.clone());
                for possibility_t2 in possibilities.iter() {
                    reverse_1_2.entry((*possibility_t2).clone()).or_insert((*possibility).clone());
                }
            }

            let mut reverse_2_3 = HashMap::<Vec<u64>, Vec<u64>>::new();
            let mut requested_moves_after3 = vec![];

            for possibility in prune(requested_moves_after2).iter() {
                let mut current = 5;
                let possibilities = possibility.iter().map(|next| {
                    let sequences = generate_sequence_for_next_dir(current, *next, 3);
                    current = *next;
                    sequences
                }).collect_vec();
                let possibilities = mix(possibilities);
                requested_moves_after3.append(&mut possibilities.clone());
                for possibility_t3 in possibilities.iter() {
                    reverse_2_3.entry((*possibility_t3).clone()).or_insert((*possibility).clone());
                }
            }

            let mut reverse_3_4 = HashMap::<Vec<u64>, Vec<u64>>::new();
            let mut requested_moves_after4 = vec![];

            for possibility in prune(requested_moves_after3).iter() {
                let mut current = 5;
                let possibilities = possibility.iter().map(|next| {
                    let sequences = generate_sequence_for_next_dir(current, *next, 3);
                    current = *next;
                    sequences
                }).collect_vec();
                let possibilities = mix(possibilities);
                requested_moves_after4.append(&mut possibilities.clone());
                for possibility_t4 in possibilities.iter() {
                    reverse_3_4.entry((*possibility_t4).clone()).or_insert((*possibility).clone());
                }
            }

            let best_len_round_4 = reverse_3_4.keys().map(|key| key.len()).min().unwrap();
            let tmp = reverse_3_4.iter().filter(|(key, _value)| key.len() == best_len_round_4).map(|(_key, value)| value.clone()).collect_vec();
            let best_round_3 = tmp.first().unwrap().to_vec();
            let best_round_2 = reverse_2_3[&best_round_3].clone();
            let best_round_1 = reverse_1_2[&best_round_2].clone();
            result.insert((start, end), best_round_1);
        }
    }
    // hack... could not figure out how many levels were needed, adding one consumes too much memory as is
    if let Some(x) = result.get_mut(&(1,5)){
        *x = vec![4,2,5];
    }
    result
}

fn solve_for_n_robots(n: u32, data: HashMap<String, u64>) -> u64 {
    let mut result = 0;
    let known_moves = build_movements();
    for (code, value) in data.iter().sorted() {
        let mut current = 2;
        let possibilities = code.chars().map(|digit_or_a| get_next_digit(digit_or_a)).map(|position| {
            let sequences = generate_sequence_for_next_dir(current, position, 0);
            current = position;
            sequences
        }).collect_vec();

        let requested_moves = prune(mix(possibilities));
        let mut requested_moves_map = Vec::<HashMap<Vec<u64>, u64>>::new();
        for possibility in requested_moves.iter() {
            let mut map = HashMap::<Vec<u64>, u64>::new();
            for elem in possibility.split(|num| *num == 5).map(|elem| elem.to_vec()).collect_vec().iter() {
                *map.entry([elem.clone(), vec![5]].concat()).or_insert(0) += 1;
            }
            requested_moves_map.push(map);
        }

        for _ in 0..n {
            for map in requested_moves_map.iter_mut() {
                let mut new_requested_moves = HashMap::<Vec<u64>, u64>::new();
                for (elem, value) in map.iter() {
                    let mut current: u64 = 5;
                    for next in elem.iter() {
                        let new_moves = known_moves.get(&(current, *next)).unwrap();
                        current = *next;
                        *new_requested_moves.entry(new_moves.clone()).or_insert(0) += value;
                    }
                }
                *map = new_requested_moves;
            }
        }
        result += *value * (requested_moves_map.iter().map(|map| map.iter().map(|(key, values)| values * key.len() as u64).sum::<u64>()).min().unwrap() - 1);
    }
    result
}
