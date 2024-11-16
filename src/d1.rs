use std::cmp;
use std::fs;

use itertools::Itertools;
use ndarray::{arr2, Array2};
use regex::Regex;

#[derive(Debug)]
pub struct D1Solver {
    pub data: Vec<(Array2<i32>, i32)>,
}

impl D1Solver {
    pub fn extract_info(&mut self, input: String) {
        let re: Regex = Regex::new(r"(?<direction>[RL])(?<count>\d+)").unwrap();

        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        let instructions: Vec<(Array2<i32>, i32)> = re.captures_iter(&contents.as_str()).map(|captures| {
            let direction: &str = captures.name("direction").unwrap().as_str();
            let direction_matrix: Array2<i32> =  if direction.eq("R") {
                arr2(&[[0, 1], [-1, 0]])
            } else {
                arr2(&[[0, -1], [1, 0]])
            };
            let count: &str = captures.name("count").unwrap().as_str();
            let count: i32 = count.to_string().parse().unwrap();
            (direction_matrix, count)
        }).collect();

        self.data = instructions;
    }

    pub fn solve_p1(&self) -> u32 {
        let mut position: Array2<i32> = arr2(&[[0], [0]]);
        let mut direction: Array2<i32> = arr2(&[[1], [0]]);

        for (rotation, distance) in self.data.iter() {
            direction = rotation.dot(&direction);
            let distance_mat: Array2<i32> = arr2(&[[*distance, 0], [0, *distance]]);
            position = position + distance_mat.dot(&direction);
        }

        f_distance(position)
    }

    pub fn solve_p2(&self) -> u32 {
        let mut position: Array2<i32> = arr2(&[[0], [0]]);
        let mut direction: Array2<i32> = arr2(&[[0], [1]]);
        let mut visited: Vec<Array2<i32>> = vec![];

        for (rotation, distance) in self.data.iter() {
            direction = rotation.dot(&direction);
            let distance_mat: Array2<i32> = arr2(&[[*distance, 0], [0, *distance]]);
            let new_position: Array2<i32> = &position + distance_mat.dot(&direction);
            if visited.len() < 3 {
                visited.push(position.clone());
                position = new_position;
                continue;
            }
            for (position1, position2) in visited.clone().into_iter().tuple_windows() {
                if f_intersect(&position1, &position2, &position, &new_position) {
                    let x: i32;
                    let y: i32;
                    if position1[[0, 0]] == position2[[0, 0]] {
                        x = position1[[0, 0]];
                        y = position[[1, 0]];
                    } else {
                        x = position[[0, 0]];
                        y = position1[[1, 0]];
                    }
                    let intersection = arr2(&[[x], [y]]);
                    return f_distance(intersection);
                }
            }
            visited.push(position.clone());
            position = new_position;
        }
        f_distance(position)
    }
}

impl Default for D1Solver {
    fn default() -> D1Solver {
        D1Solver {data : Vec::new()}
    }
}

fn f_distance(position: Array2<i32>) -> u32{
    let x:u32 = position[[0, 0]].abs().try_into().unwrap();
    let y:u32 = position[[1, 0]].abs().try_into().unwrap();

    x + y
}

fn f_side(position1: &Array2<i32>, position2: &Array2<i32>, position3: &Array2<i32>) -> i32 {
    return (position2[[1, 0]] - position1[[1, 0]]) * (position3[[0, 0]] - position2[[0, 0]]) - (position2[[0, 0]] - position1[[0, 0]]) * (position3[[1, 0]] - position2[[1, 0]])
}

fn f_is_on_segment(position1: &Array2<i32>, position2: &Array2<i32>, position3: &Array2<i32>) -> bool {
    if f_side(&position1, &position2, &position3) == 0 {
        if (position3[[0, 0]] <= cmp::max(position1[[0, 0]], position2[[0, 0]])) &&
           (position3[[0, 0]] >= cmp::min(position1[[0, 0]], position2[[0, 0]])) &&
           (position3[[1, 0]] <= cmp::max(position1[[1, 0]], position2[[1, 0]])) &&
           (position3[[1, 0]] >= cmp::min(position1[[1, 0]], position2[[1, 0]])) {
            return true
        }
    }
    false
}

fn f_intersect(position1: &Array2<i32>, position2: &Array2<i32>, position3: &Array2<i32>, position4: &Array2<i32>) -> bool {
    let d1: i32 = f_side(&position1, &position2, &position3);
    let d2: i32 = f_side(&position1, &position2, &position4);
    let d3: i32 = f_side(&position3, &position4, &position1);
    let d4: i32 = f_side(&position3, &position4, &position2);

    if ((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0)) && ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0)) {
        return true;
    } else {
        return f_is_on_segment(&position1, &position2, &position3) || f_is_on_segment(&position3, &position4, &position1);
    }
}

