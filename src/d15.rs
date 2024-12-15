use std::fs;

#[derive(Debug)]
pub struct D15Solver {
    pub moves: String,
    pub map: String,
    pub height: i32,
    pub width: i32
}

impl D15Solver {
    pub fn extract_info(&mut self, input: String) {

        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        let instructions: Vec<&str> = contents.split("\n\n").collect();

        self.map = instructions[0].replace("\n", "");
        self.moves = instructions[1].replace("\n", "");

        self.width = contents.find('\n').unwrap() as i32;
        self.height = self.map.len() as i32 / self.width;
    }

    pub fn solve_p1(&self) -> i32 {
        let mut map = self.map.clone();
        let mut robot = self.map.find('@').unwrap() as i32;

        for instruction in self.moves.chars() {
            let direction = get_dir(instruction, self.width);
            if test_push(robot, direction, &map) {
                perform_push(robot, direction, &mut map);
                robot += direction;
            }
        }

        map.char_indices()
            .filter(| (_index, character) | *character == 'O')
            .fold(0, | acc, (indx, _character) | {
                let (x, y) = (indx as i32 % self.width, indx as i32 / self.width);
                acc + ( x  + y * 100)
            })
    }

    pub fn solve_p2(&self) -> i32 {
        let mut map = self.map.clone().replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.");
        let width = self.width * 2;
        let mut robot = map.find('@').unwrap() as i32;

        for instruction in self.moves.chars() {
            let direction = get_dir(instruction, width);
            if test_push(robot, direction, &map) {
                perform_push(robot, direction, &mut map);
                robot += direction;
            }
        }

        map.char_indices()
            .filter(| (_index, character) | *character == '[')
            .fold(0, | acc, (indx, _character) | {
                let (x, y) = (indx as i32 % width, indx as i32 / width);
                acc + ( x  + y * 100)
            })
    }
}

impl Default for D15Solver {
    fn default() -> D15Solver {
        D15Solver {moves: String::default(), map: String::default(), height: i32::default(), width: i32::default()}
    }
}

fn get_dir(command: char, width: i32) -> i32 {
    match command {
        '<' => -1,
        '>' => 1,
        '^' => -width,
        'v' => width,
        _ => 0
    }
}

fn test_push(position: i32, direction: i32, map: &String) -> bool {
    let current = map.chars().nth(position as usize).unwrap();
    if current == '#' {
        return false;
    }
    let next = map.chars().nth((position + direction) as usize).unwrap();
    let mut result = true;
    match next {
        '.' => {
            result = true;
        },
        'O' => {
            result = test_push(position + direction, direction, map);
        },
        '[' => {
            result &= test_push(position + direction, direction, map);
            if direction.abs() != 1 {
                result &= test_push(position + direction + 1, direction, map);
            }
        },
        ']' => {
            result &= test_push(position + direction, direction, map);
            if direction.abs() != 1 {
                result &= test_push(position + direction - 1, direction, map);
            }
        },
        _ => {
            result = false
        }
    }
    result
}

fn perform_push(position: i32, direction: i32, map: &mut String) {
    let current = map.chars().nth(position as usize).unwrap();
    if current == '#' {
        return;
    }
    let next = map.chars().nth((position + direction) as usize).unwrap();
    match next {
        'O' => {
            perform_push(position + direction, direction, map);
        },
        '[' => {
            perform_push(position + direction, direction, map);
            if direction.abs() != 1 {
                perform_push(position + direction + 1, direction, map);
            }
        },
        ']' => {
            perform_push(position + direction, direction, map);
            if direction.abs() != 1 {
                perform_push(position + direction - 1, direction, map);
            }
        },
        _ => {}
    }
    map.replace_range((position + direction) as usize..(position + direction + 1) as usize, &String::from(current));
    map.replace_range(position as usize..(position + 1) as usize, &String::from('.'));
}
