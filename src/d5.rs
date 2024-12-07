use std::{collections::{HashMap, HashSet}, fs};

use itertools::Itertools;
use regex::{self, Regex};

#[derive(Debug)]
pub struct Data {
    pub order: HashMap<i32, HashSet<i32>>,
    pub paging: Vec<Vec<i32>>
}

#[derive(Debug)]
pub struct D5Solver {
    pub data: Data,
}

impl D5Solver {
    pub fn extract_info(&mut self, input: String) {
        let re_order = Regex::new(r"(?<num1>\d{2})\|(?<num2>\d{2})").unwrap();
        let re_paging = Regex::new(r"\d{2},(?:\d{2},?)+").unwrap();
        let re_num = Regex::new(r"(?<num>\d{2})").unwrap();

        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.data.order.clear();
        self.data.paging.clear();

        for capture in re_order.captures_iter(&contents) {
            let (first, second) = (capture.name("num1").unwrap().as_str().parse::<i32>().unwrap(), capture.name("num2").unwrap().as_str().parse::<i32>().unwrap());
            self.data.order.entry(first).or_insert(HashSet::new()).insert(second);
        }

        self.data.paging = re_paging.captures_iter(&contents).map(|capture| {
            re_num.captures_iter(capture.get(0).unwrap().as_str()).map(|cap| cap.name("num").unwrap().as_str().parse::<i32>().unwrap()).collect_vec()
        }).collect();
    }

    pub fn solve_p1(&self) -> i32 {
        let mut result = 0;
        for paging in self.data.paging.iter() {
            if is_valid(paging, &self.data.order) {
                result += paging[paging.len()/2];
            }
        }
        result
    }

    pub fn solve_p2(&self) -> i32 {
        let mut result = 0;
        let mut data = self.data.paging.clone();
        for paging in data.iter_mut() {
            if !is_valid(paging, &self.data.order) {
                repair(paging, &self.data.order);
                result += paging[paging.len()/2];
            }
        }
        result
    }
}

impl Default for D5Solver {
    fn default() -> D5Solver {
        D5Solver {data : Data { order: HashMap::new(), paging: vec![]}}
    }
}

fn is_valid(paging: &[i32], order: &HashMap<i32, HashSet<i32>>) -> bool {
    let mut result = true;
    'external: for indx in 0..paging.len() {
        let current = paging[paging.len() - indx - 1];
        if order.contains_key(&current) {
            for elem in paging[..(paging.len() - indx - 1)].iter() {
                if order.get(&current).unwrap().contains(elem) {
                    result = false;
                    break 'external;
                }
            }
        }
    }
    result
}

fn repair(paging: &mut [i32], order: &HashMap<i32, HashSet<i32>>) {
    if paging.len() == 0 {return;}
    let length  = paging.len();
    if !is_valid(&paging[1..], order) {
        repair(&mut paging[1..], order);
    }
    if !is_valid(&paging[..length - 1], order) {
        repair(&mut paging[..length - 1], order);
    }
    if order.get(&paging[length - 1]).is_some() {
        if order.get(&paging[length - 1]).unwrap().contains(&paging[0]) {
            let tmp = paging[0];
            paging[0] = paging[length - 1];
            paging[length - 1] = tmp;
        }
    }
    if !is_valid(&paging[..], order) {
        repair(paging, order);
    }
}
