use std::{collections::{BinaryHeap, VecDeque}, fs};

#[derive(Debug)]
pub struct D16Solver {
    pub nodes: Vec<Node>,
    pub width: usize,
    pub start: usize,
    pub end: usize,
}

#[derive(Eq, Ord, PartialEq, PartialOrd)]
#[derive(Clone)]
#[derive(Debug)]
pub struct Node {
    pub neighbours: Vec<usize>,
    pub value: char,
    pub cost: usize,
    pub heuristic: usize
}

impl D16Solver {
    pub fn extract_info(&mut self, input: String) {
        let mut contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.nodes.clear();

        self.width = contents.find('\n').unwrap();
        contents = contents.replace("\n", "");
        self.start = contents.find('S').unwrap();
        self.end = contents.find('E').unwrap();

        let contents = contents.as_str();

        // create all nodes with their neighbour
        for (index, character) in contents.chars().into_iter().enumerate() {
            let mut new_node = Node {neighbours: vec![], value: character, cost: usize::MAX, heuristic: heuristic(index, self.width)};
            if character == '#' {
                self.nodes.push(new_node);
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
            self.nodes.push(new_node);
        }
        a_star(&mut self.nodes, self.start, self.width, 1);
    }

    pub fn solve_p1(&self) -> usize {
        self.nodes[self.end].cost
    }

    pub fn solve_p2(&self) -> u32 {
        0
    }
}

impl Default for D16Solver {
    fn default() -> D16Solver {
        D16Solver {nodes : vec![], width: usize::default(), start: usize::default(), end: usize::default()}
    }
}

fn is_neightbour_valid(contents: &str, index2: usize) -> bool {
    contents.get(index2..index2 + 1).unwrap() != "#"
}

fn heuristic(node: usize, width: usize) -> usize {
    (node / width) + (width - node % width)
}

fn a_star(graph: &mut Vec<Node>, start: usize, width: usize, direction: i32) {
    let mut closed_list = VecDeque::<usize>::new();
    let mut open_list = BinaryHeap::<(usize, usize, i32, Node)>::new();
    open_list.push((usize::MAX - graph[start].heuristic, start, direction, graph[start].clone()));
    while !(open_list.len() == 0) {
        let (_cost, current_node_index, direction, current_node) = open_list.pop().unwrap();
        // println!("PROCESSING {current_node_index} {direction}");
        for neightbour in current_node.neighbours.iter() {
            let new_direction = *neightbour as i32 - current_node_index as i32;
            let mut new_cost = current_node.cost + 1;
            if new_direction != direction {
                new_cost += 1000;
            }
            if !closed_list.contains(neightbour) {
                if !open_list.iter().any(| elem | (elem.1 == *neightbour) && (elem.2 == new_direction) && (elem.3.cost <= new_cost)) {
                    graph[*neightbour].cost = new_cost;
                    graph[*neightbour].heuristic = usize::MAX - (new_cost + heuristic(*neightbour, width));
                    open_list.push((graph[*neightbour].heuristic, *neightbour, new_direction, graph[*neightbour].clone()));
                }
            }
        }
        closed_list.push_back(current_node_index);
    }
}
