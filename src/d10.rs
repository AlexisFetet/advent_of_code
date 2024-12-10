use std::{collections::HashSet, fs};

#[derive(Debug)]
pub struct Node {
    pub height: i32,
    pub neighbours: Vec<usize>
}

#[derive(Debug)]
pub struct D10Solver {
    pub nodes: Vec<Node>,
    pub known_starts: Vec<usize>
}

impl D10Solver {
    pub fn extract_info(&mut self, input: String) {
        let mut contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.nodes.clear();
        self.known_starts.clear();

        let length = contents.find('\n').unwrap();
        contents = contents.replace("\n", "");

        let contents = contents.as_str();

        for (index, character) in contents.chars().into_iter().enumerate() {
            let height = character.to_digit(10).unwrap() as i32;
            let mut new_node = Node {height: height, neighbours: vec![]};
            // check left neightbour
            if index % length > 0 {
                if is_neightbour_valid(contents, height, index - 1) {
                    new_node.neighbours.push(index - 1);
                }
            }
            // check right neightbour
            if index % length < length - 1 {
                if is_neightbour_valid(contents, height, index + 1) {
                    new_node.neighbours.push(index + 1);
                }
            }
            // check top neightbour
            if index as i32 - length as i32 >= 0 {
                if is_neightbour_valid(contents, height, index - length) {
                    new_node.neighbours.push(index - length);
                }
            }
            // check bottom neightbour
            if index + length < contents.len() {
                if is_neightbour_valid(contents, height, index + length) {
                    new_node.neighbours.push(index + length);
                }
            }
            self.nodes.push(new_node);
            if height == 0 {
                self.known_starts.push(index);
            }
        }
    }

    pub fn solve_p1(&self) -> usize {
        self.known_starts.iter().fold(0, | acc, node | {
            acc + dfs(&self.nodes, &mut HashSet::new(), *node, 1)
        })
    }

    pub fn solve_p2(&self) -> usize {
        self.known_starts.iter().fold(0, | acc, node | {
            acc + dfs(&self.nodes, &mut HashSet::new(), *node, 2)
        })
    }
}

impl Default for D10Solver {
    fn default() -> D10Solver {
        D10Solver {nodes: vec![], known_starts: vec![]}
    }
}

fn is_neightbour_valid(contents: &str, height: i32, index2: usize) -> bool {
    (contents.get(index2..index2 + 1).unwrap().parse::<i32>().unwrap() - height).abs() == 1
}

fn dfs(data: &Vec<Node>, visited: &mut HashSet<usize>, node: usize, part: i32) -> usize {
    let mut result = 0;
    visited.insert(node);
    if data[node].height == 9 {
        return 1;
    }
    for neightbour in data[node].neighbours.iter() {
        if data[node].height < data[*neightbour].height {
            if part == 2 || !visited.contains(neightbour) {
                result += dfs(data, visited, *neightbour, part);
            }
        }
    }
    result
}
