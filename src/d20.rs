use std::{collections::{BinaryHeap, VecDeque}, fs};

use itertools::Itertools;

#[derive(Debug)]
pub struct D20Solver {
    pub path: VecDeque<usize>,
    pub length: usize,
    pub width: usize
}

#[derive(Eq, Ord, PartialEq, PartialOrd)]
#[derive(Clone)]
#[derive(Debug)]
pub struct Node {
    pub neighbours: Vec<usize>,
    pub value: char,
    pub cost: usize,
    pub best_from: Vec<usize>,
    pub heuristic: usize
}

impl D20Solver {
    pub fn extract_info(&mut self, input: String) {
        let mut contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");
    
            self.width = contents.find('\n').unwrap();
            contents = contents.replace("\n", "");
            self.length = contents.len();
            let start = contents.find('S').unwrap();
            let end = contents.find('E').unwrap();
            let mut nodes = vec![];
    
            let contents = contents.as_str();
            // create all nodes with their neighbour
            for (index, character) in contents.chars().into_iter().enumerate() {
                let mut new_node = Node {neighbours: vec![], value: character, cost: usize::MAX, heuristic: heuristic(index, self.width, end), best_from: vec![]};
                if character == '#' {
                    nodes.push(new_node);
                    continue;
                } else if character == 'S' {
                    new_node.cost = 0;
                }
                // check left neightbour
                if index % self.width > 0 {
                    if is_neightbour_valid(contents, index - 1) {
                        new_node.neighbours.push(index - 1);
                    }
                }
                // check right neightbour
                if index % self.width < self.width - 1 {
                    if is_neightbour_valid(contents, index + 1) {
                        new_node.neighbours.push(index + 1);
                    }
                }
                // check top neightbour
                if index as i32 - self.width as i32 >= 0 {
                    if is_neightbour_valid(contents, index - self.width) {
                        new_node.neighbours.push(index - self.width);
                    }
                }
                // check bottom neightbour
                if index + self.width < contents.len() {
                    if is_neightbour_valid(contents, index + self.width) {
                        new_node.neighbours.push(index + self.width);
                    }
                }
                nodes.push(new_node);
            }
            a_star(&mut nodes, start, end,  self.width);


            let mut visited = VecDeque::<usize>::new();
            let mut processing_queue = VecDeque::<usize>::new();
            processing_queue.push_back(end);
            while processing_queue.len() != 0 {
                let current = processing_queue.pop_front().unwrap();
                visited.push_back(current);
                let current_node = nodes[current].clone();
                for neightbour in current_node.best_from.iter() {
                    if !visited.contains(&neightbour) && !processing_queue.contains(neightbour) {
                    processing_queue.push_back(*neightbour);

                    }
                }
            }
            self.path = visited;

    }

    pub fn solve_p1(&self) -> u32 {
        cheat_count(self.path.clone(), 2, self.length, self.width, 100)
    }

    pub fn solve_p2(&self) -> u32 {
        cheat_count(self.path.clone(), 20, self.length, self.width, 100)
    }
}

impl Default for D20Solver {
    fn default() -> D20Solver {
        D20Solver {path : VecDeque::<usize>::new(), length: 0, width: 0 }
    }
}
fn is_neightbour_valid(contents: &str, index2: usize) -> bool {
    contents.get(index2..index2 + 1).unwrap() != "#"
}

fn heuristic(node: usize, width: usize, end: usize) -> usize {
    (node / width).abs_diff(end / width) + (width - node % width).abs_diff(width - end % width)
}

fn a_star(graph: &mut Vec<Node>, start: usize, end: usize, width: usize) {
    let mut closed_list = VecDeque::<usize>::new();
    let mut open_list = BinaryHeap::<(usize, usize, Node)>::new();
    open_list.push((usize::MAX - graph[start].heuristic, start, graph[start].clone()));
    while !(open_list.len() == 0) {
        let (_cost, current_node_index, current_node) = open_list.pop().unwrap();
        for neightbour in current_node.neighbours.iter() {
            let mut neightbour_node = graph[*neightbour].clone();
            let new_cost = current_node.cost + 1;
            neightbour_node.cost = new_cost;
            neightbour_node.heuristic = usize::MAX - (new_cost + heuristic(*neightbour, width, end));
            if graph[*neightbour].cost == new_cost {
                graph[*neightbour].best_from.push(current_node_index);
            } else if graph[*neightbour].cost > new_cost {
                graph[*neightbour].best_from = vec![current_node_index];
            }
            if !closed_list.contains(neightbour) {
                if !open_list.iter().any(| (_heuristic, index, node) | (index == neightbour) && (node.cost < neightbour_node.cost)) {
                    graph[*neightbour].cost = neightbour_node.cost;
                    graph[*neightbour].heuristic = neightbour_node.heuristic;
                    open_list.push((neightbour_node.heuristic, *neightbour, neightbour_node));
                }
            }
        }
        closed_list.push_back(current_node_index);
    }
}

fn cheat_count(path: VecDeque<usize>, range: i32, length: usize, width: usize, threshold: i32) -> u32 {
    let mut count = 0;
    let mut queue = path.clone();
    let mut current_index = 0;
    let max_x = width as i32 - 1;
    let max_y = length as i32 / width as i32;
    while queue.len() != 0 {
        let current = queue.pop_front().unwrap() as i32;
        let current_x = current % width as i32;
        let current_y = current / width as i32;
        for delta_x in -range..=range {
            for delta_y in -(range - delta_x)..=(range - delta_x) {
                let (new_x, new_y) = (current_x + delta_x, current_y + delta_y);
                if (0 <= new_x && new_x <= max_x) && (0 <= new_y && new_y <= max_y) {
                    let distance = (delta_x).abs() + (delta_y).abs();
                    if distance <= range {
                        let maybe_on_path = path.iter().find_position(|element| **element == (new_x as usize + new_y as usize * width));
                        if maybe_on_path.is_some() {
                            let (new_index, _current) = maybe_on_path.unwrap();
                            if new_index as i32 - current_index as i32 - distance >= threshold {
                                count += 1;
                            }
                        }
                    }
                }
            }
        }
        current_index += 1;
    }
    count
}
