use std::fs;

use itertools::Itertools;

#[derive(Debug)]
pub struct D6Solver {
    pub data: Vec<(i32, i32)>,
    pub starting_point: (i32, i32),
    pub x_max: i32,
    pub y_max: i32
}

impl D6Solver {
    pub fn extract_info(&mut self, input: String) {
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.data.clear();
        self.x_max = contents.lines().nth(0).unwrap().len() as i32 - 1;
        self.y_max = match contents.lines().nth(0).unwrap().chars().try_len() {
            Ok(size) => size as i32, 
            Err((_, hint)) => hint.unwrap() as i32
        } - 1;

        for (y, line) in contents.lines().enumerate() {

            for (x, character) in line.chars().enumerate() {
                if character == '#' {
                    self.data.push((x as i32, y as i32));
                } else if character == '^' {
                    self.starting_point = (x as i32, y as i32);
                }
            }
        }
    }

    pub fn solve_p1(&self) -> u32 {
        let (visited_positions, _finish_in_bound) = get_path(&self.data, self.starting_point, self.x_max, self.y_max);
        visited_positions.len() as u32
    }

    pub fn solve_p2(&self) -> i32 {
        let mut result = 0;
        let mut data = self.data.clone();
        let (visited_positions, _finish_in_bound) = get_path(&self.data, self.starting_point, self.x_max, self.y_max);
        for (x_injected, y_injected) in visited_positions.iter() {
            if (*x_injected, *y_injected) != self.starting_point {
                data.push((*x_injected, *y_injected)); // prevent always copying the vec
                let (_visited_positions, finish_in_bound) = get_path(&data, self.starting_point, self.x_max, self.y_max);
                if finish_in_bound {
                    result += 1;
                }
                data.pop(); // clean
            }
        }
        result
    }
}

impl Default for D6Solver {
    fn default() -> D6Solver {
        D6Solver {data : vec![], starting_point: (0, 0), x_max: 0, y_max: 0}
    }
}

fn is_in_bound(x: i32, y: i32, x_max: i32, y_max: i32) -> bool {
    (0 <= x) && (x <= x_max) && (0 <= y) && (y <= y_max)
}

fn turn_right(direction: &mut(i32, i32)) {
    let x = direction.0;
    direction.0 = -direction.1;
    direction.1 = x;
}

fn get_path(data: &Vec<(i32, i32)>, starting_point: (i32, i32), x_max: i32, y_max: i32) -> (Vec<(i32, i32)>, bool) {
    let mut current = starting_point;
    let mut direction = (0, -1);
    let mut visited_states = vec![];
    while is_in_bound(current.0, current.1, x_max, y_max) && !visited_states.contains(&(current.0, current.1, direction.0, direction.1)) {
        if !data.contains(&(current.0 + direction.0, current.1 + direction.1)) {
            visited_states.push((current.0, current.1, direction.0, direction.1));
            current.0 = current.0 + direction.0;
            current.1 = current.1 + direction.1;
        } else {
            visited_states.push((current.0, current.1, direction.0, direction.1));
            turn_right(&mut direction);
        }
    }
    let mut visited_locations = visited_states.iter().map(|(x, y, _dirx, _diry)| (*x, *y)).collect_vec();
    visited_locations.sort();
    visited_locations.dedup();
    (visited_locations, is_in_bound(current.0, current.1, x_max, y_max))
}
