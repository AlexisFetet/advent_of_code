use std::fs;

use regex::Regex;

#[derive(PartialEq)]
#[derive(Debug)]
pub struct Drone {
    pub x: i32,
    pub y: i32,
    pub vx: i32,
    pub vy: i32,
}

#[derive(Debug)]
pub struct D14Solver {
    pub drones: Vec<Drone>,
}

impl D14Solver {
    pub fn extract_info(&mut self, input: String) {
        let re = Regex::new(r"p=(?<x>\d+),(?<y>\d+) v=(?<vx>-?\d+),(?<vy>-?\d+)").unwrap();

        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.drones = re.captures_iter(&contents).map(| capture | Drone {
            x: capture.name("x").unwrap().as_str().parse::<i32>().unwrap(),
            y: capture.name("y").unwrap().as_str().parse::<i32>().unwrap(),
            vx: capture.name("vx").unwrap().as_str().parse::<i32>().unwrap(),
            vy: capture.name("vy").unwrap().as_str().parse::<i32>().unwrap(),
        }).collect();
    }

    pub fn solve_p1(&self, width: i32, height: i32) -> u32 {
        let mut drones = self.drones.clone();
        for _ in 0..100 {
            move_drones(&mut drones, width, height);
        }
        let (mid_x, mid_y) = (width / 2, height / 2);
        let (mut top_left, mut top_right, mut bot_left, mut bot_right) = (0, 0, 0, 0);
        let mut iteration = vec![
                (&mut top_left, 0, mid_x - 1, 0, mid_y - 1),
                (&mut top_right, width - mid_x, width, 0, mid_y - 1),
                (&mut bot_left, 0, mid_x - 1, height - mid_y, height),
                (&mut bot_right, width - mid_x, width, height - mid_y, height)
            ];
        for drone in drones.iter() {
            for (quadrand, x_min, x_max, y_min, y_max) in iteration.iter_mut() {
                if *x_min <= drone.x && drone.x <= *x_max && *y_min <= drone.y && drone.y <= *y_max {
                    **quadrand = **quadrand + 1;
                    break;
                }
            }
        }
        top_left * top_right * bot_left * bot_right
    }

    pub fn solve_p2(&self, width: i32, height: i32) -> usize {
        let mut drones = self.drones.clone();
        // assuming tree is in the middle and will cause all robots to gather aroud the middle
        let (mid_x, mid_y) = (width / 2, height / 2);
        let mut dispersions = vec![];
        // the input is nice enough to have a cycle
        while drones != self.drones || dispersions.is_empty() {
            dispersions.push(compute_dispersion_sum(&drones, mid_x, mid_y));
            move_drones(&mut drones, width, height);
        }
        // compute dispersion for the last move we did
        dispersions.push(compute_dispersion_sum(&drones, mid_x, mid_y));
        let min_value = dispersions.iter().min().unwrap();
        dispersions.iter().position(| elem | elem == min_value).unwrap()
    }
}

impl Default for D14Solver {
    fn default() -> D14Solver {
        D14Solver {drones : vec![]}
    }
}

impl Clone for Drone {
    fn clone(&self) -> Drone {
        Drone {x: self.x, y: self.y, vx: self.vx, vy: self.vy}
    }
}

fn compute_dispersion_sum(drones: &Vec<Drone>, mid_x: i32, mid_y: i32) -> i32 {
    drones.iter().fold(0, |acc, drone| acc + (drone.x-mid_x).pow(2) + (drone.y-mid_y).pow(2))
}

fn move_drones(drones: &mut Vec<Drone>, width: i32, height: i32) {
    for drone in drones.iter_mut() {
        drone.x = (drone.x + drone.vx).rem_euclid(width);
        drone.y = (drone.y + drone.vy).rem_euclid(height);
    }
}
