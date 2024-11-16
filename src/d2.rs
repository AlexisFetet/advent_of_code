use std::{char, fs};

use ndarray::{arr2, Array2};

#[derive(Debug)]
pub struct D2Solver {
    pub data: Vec<String>,
}

impl D2Solver {
    pub fn extract_info(&mut self, input: String) {
        self.data = fs::read_to_string(input)
            .unwrap()
            .lines()
            .map(String::from)
            .collect();
    }

    pub fn solve_p1(&self) -> String {
        let mut result: String = String::from("");
        let mut position = arr2(&[[0], [0]]);
        for row in self.data.iter() {
            for command in row.chars() {
                f_move(&mut position, command, 0);
            }
            result.push_str(&f_give_digit(&position, 0));
        }
        result
    }

    pub fn solve_p2(&self) -> String {
        let mut result: String = String::from("");
        let mut position = arr2(&[[-2], [0]]);
        for row in self.data.iter() {
            for command in row.chars() {
                f_move(&mut position, command, 1);
            }
            result.push_str(&f_give_digit(&position, 1));
        }
        result
    }
}

impl Default for D2Solver {
    fn default() -> D2Solver {
        D2Solver {data : vec![]}
    }
}

fn f_clamp(position: &mut Array2<i32>, initial_position: &Array2<i32>, slope: i32) {
    let max_dir: i32 = 1 + slope;
    if (position[[0, 0]].abs() > max_dir) || (position[[1, 0]].abs() > max_dir) {
        *position = initial_position.clone();
        return
    } else if (slope == 1) && ((position[[0, 0]].abs() + position[[1, 0]].abs()) > max_dir) {
        *position = initial_position.clone();
        return
    }

}

fn f_give_digit(position: &Array2<i32>, slope: i32) -> String{
    let mut digit: i32;
    if slope == 0 {
        digit = ((position[[0, 0]] + 2) + 3 * (1 - position[[1, 0]])).try_into().unwrap();
    } else {
        match position[[1, 0]] {
            2 => digit = 1,
            1 => digit = 3,
            0 => digit = 7,
            -1 => digit = 11,
            -2 => digit = 13,
            _ => panic!("Unkown command!"),
        }
        digit = digit + position[[0, 0]];
    }
    format!("{:1x}", digit)
}

fn f_move(position: &mut Array2<i32>, command: char, slope: i32) {
    let previous_position = position.clone();
    match command {
        'U' => *position = &previous_position + arr2(&[[0], [1]]),
        'D' => *position = &previous_position + arr2(&[[0], [-1]]),
        'R' => *position = &previous_position + arr2(&[[1], [0]]),
        'L' => *position = &previous_position + arr2(&[[-1], [0]]),
        _ => panic!("Unkown command!"),
    }
    f_clamp(position, &previous_position, slope);
}