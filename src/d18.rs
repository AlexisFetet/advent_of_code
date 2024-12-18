use std::{collections::{BinaryHeap, HashSet}, fs};

use itertools::Itertools;

#[derive(Debug)]
pub struct D18Solver {
    pub data: Vec<(i32, i32)>,
}

#[derive(PartialEq, Eq, PartialOrd, Ord, Hash)]
#[derive(Debug)]
pub struct Node {
    pub position: (i32, i32),
    pub cost: i32,
    pub heuristic: i32
}

impl D18Solver {
    pub fn extract_info(&mut self, input: String) {
        self.data = fs::read_to_string(input)
            .expect("Should have been able to read the file")
            .lines()
            .map(| line | {
                let mut iter = line.splitn(2, ",");
                (iter.next().unwrap().parse::<i32>().unwrap(), iter.next().unwrap().parse::<i32>().unwrap())
            }).collect_vec();
    }

    pub fn solve_p1(&self, target: i32, count: usize) -> i32 {
        let directions = [(0, 1), (0, -1), (1, 0), (-1, 0)];
        let mut closed_list = HashSet::new();
        let mut open_list = BinaryHeap::new();
        let obstacles = self.data.get(..count).unwrap();
        open_list.push((i32::MAX - 2 * target, Node{position: (0, 0), cost: 0, heuristic: 2 * target}));
        while open_list.len() != 0 {
            let (_, current) = open_list.pop().unwrap();
            if current.position == (target, target) {
                closed_list.insert(Node{position: (target, target), cost: current.cost, heuristic: 0});
                break;
            }
            for direction in directions.iter() {
                let neighbour = Node{position: (current.position.0 + direction.0, current.position.1 + direction.1), cost: current.cost + 1, heuristic: current.cost + 2 * target - (current.position.0 + direction.0) - (current.position.1 + direction.1)};
                if is_valid(neighbour.position, target) && !closed_list.iter().any(| node: &Node | node.position == neighbour.position)  && !obstacles.contains(&neighbour.position) {
                    if !open_list.iter().any(|(_, node)|{(node.position == neighbour.position) && (node.cost < neighbour.cost)}) {
                        open_list.push((i32::MAX - neighbour.heuristic, neighbour));
                    }
                }
            }
            closed_list.insert(current);
        }
        closed_list.iter().find(| node | node.position == (target, target)).unwrap().cost
    }

    pub fn solve_p2(&self, target: i32) -> (i32, i32) {
        let directions = [(0, 1), (0, -1), (1, 0), (-1, 0)];
        let mut closed_list = HashSet::new();
        let mut open_list = BinaryHeap::new();
        let mut count =  self.data.len();
        while closed_list.iter().find(|node: &&Node| node.position == (0, 0)).is_none() {
            closed_list.clear();
            open_list.clear();
            open_list.push((i32::MAX, Node{position: (target, target), cost: 0, heuristic: 2 * target}));
            count -= 1;
            let obstacles = self.data.get(..count).unwrap();
            while open_list.len() != 0 {
                let (_, current) = open_list.pop().unwrap();
                if current.position == (0, 0) {
                    closed_list.insert(Node{position: (0, 0), cost: current.cost, heuristic: 0});
                    break;
                }
                for direction in directions.iter() {
                    let neighbour = Node{position: (current.position.0 + direction.0, current.position.1 + direction.1), cost: current.cost + 1, heuristic: current.cost + (current.position.0 + direction.0) - (current.position.1 + direction.1)};
                    if is_valid(neighbour.position, target) && !closed_list.iter().any(| node: &Node | node.position == neighbour.position)  && !obstacles.contains(&neighbour.position) {
                        if !open_list.iter().any(|(_, node)|{(node.position == neighbour.position) && (node.cost < neighbour.cost)}) {
                            open_list.push((i32::MAX - neighbour.heuristic, neighbour));
                        }
                    }
                }
                closed_list.insert(current);
            }
        }
        self.data[count]
    }
}

impl Default for D18Solver {
    fn default() -> D18Solver {
        D18Solver {data : vec![]}
    }
}

fn is_valid(point: (i32, i32), width: i32) -> bool {
    0 <= point.0 && point.0 <= width && 0 <= point.1 && point.1 <= width
}
