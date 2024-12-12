use std::{collections::HashSet, fs};

#[derive(Debug)]
pub struct Node {
    pub id: usize,
    pub value: char,
    pub corner_contribution: i32,
    pub neighbours: Vec<usize>
}

#[derive(Debug)]
pub struct Garden {
    pub garden_type: char,
    pub perimeter: i32,
    pub area: i32,
    pub edges: i32,
    pub nodes: HashSet<usize>
}

#[derive(Debug)]
pub struct D12Solver {
    pub nodes: Vec<Node>,
    pub gardens: Vec<Garden>
}

impl D12Solver {
    pub fn extract_info(&mut self, input: String) {
        let mut contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.gardens.clear();
        self.nodes.clear();
        let length = contents.find('\n').unwrap();
        contents = contents.replace("\n", "");
        let contents = contents.as_str();

        // create all nodes with their neighbour of the same garden
        for (index, character) in contents.chars().into_iter().enumerate() {
            let (mut up, mut right, mut down, mut left) = (false, false, false, false);
            let mut new_node = Node {id: index, value: character, corner_contribution: 0, neighbours: vec![]};
            let mut corners = 0;
            // check left neightbour
            if index % length > 0 {
                if is_same(contents, character, index - 1) {
                    new_node.neighbours.push(index - 1);
                    left = true;
                }
            }
            // check right neightbour
            if index % length < length - 1 {
                if is_same(contents, character, index + 1) {
                    new_node.neighbours.push(index + 1);
                    right = true;
                }
            }
            // check top neightbour
            if index as i32 - length as i32 >= 0 {
                if is_same(contents, character, index - length) {
                    new_node.neighbours.push(index - length);
                    up = true;
                }
            }
            // check bottom neightbour
            if index + length < contents.len() {
                if is_same(contents, character, index + length) {
                    new_node.neighbours.push(index + length);
                    down = true;
                }
            }
            let corner_check = vec![
                // we know 3rd parameter is valid if used as this is in diagonal
                (up, left, index - length - 1),
                (up, right, index - length + 1),
                (down, left, index + length - 1),
                (down, right, index + length + 1)
            ];
            // count corners (nb corners = nb sides)
            for (dir1, dir2, extra_check) in corner_check.iter() {
                match (dir1, dir2) {
                    (true, true) => {
                        if !is_same(contents, character, *extra_check) {
                            corners += 1
                        }
                    },
                    (false, false) => corners += 1,
                    (_, _) => {}
                }
            }
            new_node.corner_contribution = corners;
            self.nodes.push(new_node);
        }

        // create all gardens
        let mut visited_nodes: HashSet<usize> = HashSet::new();
        for node in self.nodes.iter() {
            if visited_nodes.contains(&node.id) {
                continue;
            }
            let mut garden = Garden{garden_type: node.value, perimeter: 0, area: 0, edges: 0, nodes: HashSet::new()};
            // fill garden nodes, perimeter and area
            (garden.perimeter, garden.edges) = dfs(&self.nodes, &mut garden, node.id);
            garden.area = garden.nodes.len() as i32;
            visited_nodes.extend(garden.nodes.clone());
            self.gardens.push(garden);
        }
    }

    pub fn solve_p1(&self) -> i32 {
        self.gardens.iter().fold(0, |acc, garden| acc + garden.perimeter * garden.area)
    }

    pub fn solve_p2(&self) -> i32 {
        self.gardens.iter().fold(0, |acc, garden| acc + garden.edges * garden.area)
    }
}

impl Default for D12Solver {
    fn default() -> D12Solver {
        D12Solver {nodes : vec![], gardens: vec![]}
    }
}

fn is_same(contents: &str, character: char, index2: usize) -> bool {
    contents.get(index2..index2 + 1).unwrap().chars().nth(0).unwrap() == character
}

fn dfs(data: &Vec<Node>, visiting: &mut Garden, node: usize) -> (i32, i32) {
    let mut perimeter_contribution = 4 - data[node].neighbours.len() as i32;
    let mut corner_contribution = data[node].corner_contribution;
    visiting.nodes.insert(node);
    for neightbour in data[node].neighbours.iter() {
        if !visiting.nodes.contains(neightbour) {
            let (perimeter_contribution_child, corner_contribution_child) = dfs(data, visiting, *neightbour);
            perimeter_contribution += perimeter_contribution_child;
            corner_contribution += corner_contribution_child;
        }
    }
    (perimeter_contribution, corner_contribution)
}
