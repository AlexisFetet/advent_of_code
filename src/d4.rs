use std::fs;

#[derive(Debug)]
pub struct D4Solver {
    pub data: Vec<String>,
}

impl D4Solver {
    pub fn extract_info(&mut self, input: String) {
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");
        self.data = contents.lines().map(|f| String::from(f)).collect();
    }

    pub fn solve_p1(&self) -> u32 {
        let mut result = 0;
        for x in 0..self.data.len() {
            for y in 0..self.data[0].len() {
                if get(&self.data, x as i32, y as i32) == 'X' {
                    for x_dir in -1..2 {
                        for y_dir in -1..2 {
                            result += find_dir(&self.data, x as i32, y as i32, x_dir as i32, y_dir as i32, vec!['M', 'A', 'S']);
                        }
                    }
                }
            }
        }
        result
    }

    pub fn solve_p2(&self) -> u32 {
        let mut result = 0;
        for x in 0..self.data.len() {
            for y in 0..self.data[0].len() {
                if get(&self.data, x as i32, y as i32) == 'A' {
                    result += find_x(&self.data, x as i32, y as i32);
                }
            }
        }
        result
    }
}

impl Default for D4Solver {
    fn default() -> D4Solver {
        D4Solver {data : vec![]}
    }
}

fn get(data: &Vec<String>, x: i32, y: i32) -> char {
    let mut result = '.';
    if x < 0 || y < 0 {
        return result;
    }
    let line = data.get(x as usize);
    if line.is_some_and(| line|line.len() > y as usize){
        result = line.unwrap().chars().nth(y as usize).unwrap();
    }
    result
}

fn find_dir(data: &Vec<String>, x: i32, y: i32, x_dir: i32, y_dir: i32, to_find: Vec<char>) -> u32 {
    let mut result = 0;
    if to_find.len() == 0 {return 1;}
    let target = to_find[0];
    if get(data, x + x_dir, y + y_dir) == target {
        result += find_dir(data, x + x_dir, y + y_dir, x_dir, y_dir, to_find[1..].to_vec());
    }
    result
}

fn find_x(data: &Vec<String>, x: i32, y: i32) -> u32 {
    let (char1, char2, char3, char4) = (get(data, x - 1, y - 1), get(data, x - 1, y + 1), get(data, x + 1, y + 1), get(data, x + 1, y - 1));
    for char_ in [char1, char2, char3, char4] {
        if char_ != 'M' && char_ != 'S' {
            return 0;
        }
        if char1 == char3 || char2 == char4 {
            return 0;
        }
    }
    1
}
