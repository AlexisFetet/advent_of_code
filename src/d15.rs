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
            if push(robot, direction, &mut map) {
                map.replace_range(robot as usize..(robot + 1) as usize, &String::from('.'));
                robot += direction;
            }
        }

        map.char_indices().filter(| (_index, character) | *character == 'O').fold(0, | acc, (indx, _character) | acc + (indx as i32 % self.width + (indx as i32 / self.width) * 100))
    }

    pub fn solve_p2(&self) -> u32 {
        0
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

fn push(position: i32, direction: i32, map: &mut String) -> bool {
    let current = map.chars().nth(position as usize).unwrap();
    if current == '#' {
        return false;
    }
    let next = map.chars().nth((position + direction) as usize).unwrap();
    let mut result = false;
    match next {
        '.' => {
            map.replace_range((position + direction) as usize..(position + direction + 1) as usize, &String::from(current));
            result = true;
        },
        'O' => {
            if push(position + direction, direction, map) {
                map.replace_range((position + direction) as usize..(position + direction + 1) as usize, &String::from(current));
                result = true;
            }
        },
        _ => {}
    }
    result
}
