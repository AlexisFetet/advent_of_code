use std::{collections::{HashMap, HashSet}, fs, i32};

use itertools::Itertools;

#[derive(Debug)]
pub struct D8Solver {
    pub data: HashMap<char, HashSet<(i32, i32)>>,
    pub max_x: i32,
    pub max_y: i32,
}

impl D8Solver {
    pub fn extract_info(&mut self, input: String) {
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.data.clear();
        for (y, line) in contents.lines().enumerate() {
            for (x, character) in line.chars().enumerate() {
                if character != '.' {
                    self.data.entry(character).or_insert(HashSet::new()).insert((x as i32, y as i32));
                }
            }
        }
        self.max_x = contents.lines().nth(0).unwrap().len() as i32 - 1;
        self.max_y = match contents.lines().nth(0).unwrap().chars().try_len() {
            Ok(size) => size as i32, 
            Err((_, hint)) => hint.unwrap() as i32
        } - 1;
    }

    pub fn solve_p1(&self) -> usize {
        get_antinodes_count(&self.data, self.max_x, self.max_y, 1)
    }

    pub fn solve_p2(&self) -> usize {
        get_antinodes_count(&self.data, self.max_x, self.max_y, 2)
    }
}

impl Default for D8Solver {
    fn default() -> D8Solver {
        D8Solver {data : HashMap::new(), max_x: 0, max_y: 0}
    }
}

fn is_in_bound(position: &(i32, i32), max_x: i32, max_y: i32) -> bool {
    (0 <= position.0) && (position.0 <= max_x) && (0 <= position.1) && (position.1 <= max_y)
}

fn get_antinodes_count(data: &HashMap<char, HashSet<(i32, i32)>>, max_x: i32, max_y: i32, part: i32) -> usize {
    let mut known_antinodes = HashSet::new();
    let iter_max = if part == 1 {2} else {i32::MAX};

    for antenna_positions in data.values() {
        if part == 2 {
            known_antinodes.extend(antenna_positions);
        }
        for position_vect in antenna_positions.iter().combinations(2).into_iter() {
            let (delta_x, delta_y) = (position_vect[1].0 - position_vect[0].0, position_vect[1].1 - position_vect[0].1);
            for k in 1..iter_max {
                let attempt = (position_vect[0].0 - (k * delta_x), position_vect[0].1 - (k * delta_y));
                if is_in_bound(&attempt, max_x, max_y) {
                    known_antinodes.insert(attempt);
                } else {
                    break;
                }
            }
            for k in 1..iter_max {
                let attempt = (position_vect[1].0 + (k * delta_x), position_vect[1].1 + (k * delta_y));
                if is_in_bound(&attempt, max_x, max_y) {
                    known_antinodes.insert(attempt);
                } else {
                    break;
                }
            }
        }
    }

   known_antinodes.len()
}
