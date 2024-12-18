use std::{collections::{BinaryHeap, VecDeque}, fs};

#[derive(Debug)]
pub struct D16Solver {
    pub nodes: Vec<Node>,
    pub width: usize,
    pub length: usize,
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
        self.length = contents.len();
        self.start = contents.find('S').unwrap();
        self.end = contents.find('E').unwrap();

        let contents = contents.as_str();
        let mut nodes_left_right = vec![];
        // create all nodes with their neighbour
        for (index, character) in contents.chars().into_iter().enumerate() {
            let mut new_node_up_down = Node {neighbours: vec![], value: character, cost: usize::MAX, heuristic: heuristic(index, self.width)};
            let mut new_node_left_right = Node {neighbours: vec![], value: character, cost: usize::MAX, heuristic: heuristic(index, self.width)};
            if character == '#' {
                self.nodes.push(new_node_up_down);
                nodes_left_right.push(new_node_left_right);
                continue;
            } else if character == 'S' {
                new_node_up_down.cost = 0;
                new_node_left_right.cost = 0;
            }
            // check left neightbour
            if index % self.width > 0 {
                if is_neightbour_valid(contents, index - 1) {
                    new_node_up_down.neighbours.push(index - 1);
                    new_node_left_right.neighbours.push(index - 1);
                }
            }
            // check right neightbour
            if index % self.width < self.width - 1 {
                if is_neightbour_valid(contents, index + 1) {
                    new_node_up_down.neighbours.push(index + 1);
                    new_node_left_right.neighbours.push(index + 1);
                }
            }
            // check top neightbour
            if index as i32 - self.width as i32 >= 0 {
                if is_neightbour_valid(contents, index - self.width) {
                    new_node_up_down.neighbours.push(index - self.width + self.length);
                    new_node_left_right.neighbours.push(index - self.width + self.length);
                }
            }
            // check bottom neightbour
            if index + self.width < contents.len() {
                if is_neightbour_valid(contents, index + self.width) {
                    new_node_up_down.neighbours.push(index + self.width + self.length);
                    new_node_left_right.neighbours.push(index + self.width + self.length);
                }
            }
            self.nodes.push(new_node_up_down);
            nodes_left_right.push(new_node_left_right);
        }
        self.nodes = [self.nodes.clone(), nodes_left_right].concat();
        a_star(&mut self.nodes, self.start,  self.width);
    }

    pub fn solve_p1(&self) -> usize {
        self.nodes[self.end].cost.min(self.nodes[self.end + self.length].cost)
    }

    pub fn solve_p2(&self) -> u32 {
        0
    }
}

impl Default for D16Solver {
    fn default() -> D16Solver {
        D16Solver {nodes : vec![], width: usize::default(), length: usize::default(), start: usize::default(), end: usize::default()}
    }
}

fn is_neightbour_valid(contents: &str, index2: usize) -> bool {
    contents.get(index2..index2 + 1).unwrap() != "#"
}

fn heuristic(node: usize, width: usize) -> usize {
    (node / width) + (width - node % width)
}

fn a_star(graph: &mut Vec<Node>, start: usize, width: usize) {
    let mut closed_list = VecDeque::<usize>::new();
    let mut open_list = BinaryHeap::<(usize, usize, Node)>::new();
    open_list.push((usize::MAX - graph[start].heuristic, start, graph[start].clone()));
    while !(open_list.len() == 0) {
        let (_cost, current_node_index, current_node) = open_list.pop().unwrap();
        for neightbour in current_node.neighbours.iter() {
            let mut neightbour_node = graph[*neightbour].clone();
            let mut new_cost = current_node.cost + 1;
            if (*neightbour as i64 - current_node_index as i64).abs() > (width as i64).try_into().unwrap() {
                new_cost += 1000;
            }
            neightbour_node.cost = new_cost;
            neightbour_node.heuristic = usize::MAX - (new_cost + heuristic(*neightbour, width));
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
