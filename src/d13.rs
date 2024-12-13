use std::fs;

use regex::{self, Regex};

#[derive(Debug)]
pub struct Machine {
    pub ax: i64,
    pub ay: i64,
    pub bx: i64,
    pub by: i64,
    pub x: i64,
    pub y: i64,
}


#[derive(Debug)]
pub struct D13Solver {
    pub data: Vec<Machine>,
}

impl D13Solver {
    pub fn extract_info(&mut self, input: String) {
        let re = Regex::new(r"Button A: X\+(?<ax>\d+), Y\+(?<ay>\d+)\nButton B: X\+(?<bx>\d+), Y\+(?<by>\d+)\nPrize: X=(?<x>\d+), Y=(?<y>\d+)").unwrap();

        self.data.clear();

        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.data = re.captures_iter(&contents).map(| capture | {
            Machine{
                ax: capture.name("ax").unwrap().as_str().parse::<i64>().unwrap(),
                ay: capture.name("ay").unwrap().as_str().parse::<i64>().unwrap(),
                bx: capture.name("bx").unwrap().as_str().parse::<i64>().unwrap(),
                by: capture.name("by").unwrap().as_str().parse::<i64>().unwrap(),
                x: capture.name("x").unwrap().as_str().parse::<i64>().unwrap(),
                y: capture.name("y").unwrap().as_str().parse::<i64>().unwrap(),
            }
        }).collect();
    }

    pub fn solve_p1(&self) -> i64 {
        self.data.iter().map(| machine | token_count(machine, 1)).sum()
    }

    pub fn solve_p2(&self) -> i64 {
        self.data.iter().map(| machine | token_count(machine, 2)).sum()
    }
}

impl Default for D13Solver {
    fn default() -> D13Solver {
        D13Solver {data : vec![]}
    }
}

fn token_count(machine: &Machine, part: i64) -> i64 {
    let det = machine.ax * machine.by - machine.ay * machine.bx;
    if det == 0 {
        return 0;
    }
    let a_x_det = machine.by * (10000000000000 * (part - 1) + machine.x) - machine.bx * (10000000000000 * (part - 1) + machine.y);
    let b_x_det = machine.ax * (10000000000000 * (part - 1) + machine.y) - machine.ay * (10000000000000 * (part - 1) + machine.x);
    if (a_x_det % det) != 0 || (b_x_det % det) != 0 {
        return 0;
    } else {
        return (3 * a_x_det / det) + (1 * b_x_det / det)
    }
}
