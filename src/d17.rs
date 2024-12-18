use std::fs;

use regex::Regex;

#[derive(Debug)]
pub struct D17Solver {
    pub data: CPU
}

#[derive(Clone)]
#[derive(Debug)]
pub struct CPU {
    pub register_a: u64,
    pub register_b: u64,
    pub register_c: u64,
    pub program: Vec<u64>,
    pub program_counter: usize
}

impl D17Solver {
    pub fn extract_info(&mut self, input: String) {
        let regs = Regex::new(r"Register A: (?<RA>\d+)\nRegister B: (?<RB>\d+)\nRegister C: (?<RC>\d+)").unwrap();
        let prog = Regex::new(r"Program: (?<PROG>([0-7],?)+)").unwrap();

        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.data.program_counter = 0;
        let capture = regs.captures(&contents).unwrap();
        self.data.register_a = capture.name("RA").unwrap().as_str().parse::<u64>().unwrap();
        self.data.register_b = capture.name("RB").unwrap().as_str().parse::<u64>().unwrap();
        self.data.register_c = capture.name("RC").unwrap().as_str().parse::<u64>().unwrap();
        let program = prog.captures(&contents).unwrap();
        self.data.program = program.name("PROG").unwrap().as_str().split(",").map(| digit| digit.parse().unwrap()).collect();
    }

    pub fn solve_p1(&self) -> Vec<u64> {
        let mut cpu = self.data.clone();
        let mut new_program = vec![];
        while cpu.program_counter != cpu.program.len() {
            let instruction = cpu.program[cpu.program_counter];
            cpu.program_counter = cpu.program_counter + 1;
            let maybe_instruction = match instruction {
                0 => adv(&mut cpu),
                1 => bxl(&mut cpu),
                2 => bst(&mut cpu),
                3 => jnz(&mut cpu),
                4 => bxc(&mut cpu),
                5 => out(&mut cpu),
                6 => bdv(&mut cpu),
                7 => cdv(&mut cpu),
                _ => panic!()
            };
            if maybe_instruction.is_some() {
                new_program.push(maybe_instruction.unwrap());
            }
        }
        new_program
    }

    pub fn solve_p2(&self) -> u64 {
        let mut new_program: Vec<u64> = vec![];
        let mut a_start = 0;
        let mut low_bits = 1;
        let mut shift = 3;
        while new_program != self.data.program {
            let mut cpu = self.data.clone();
            cpu.register_a = a_start + low_bits;
            new_program.clear();
            while cpu.program_counter < cpu.program.len() && new_program.len() <= self.data.program.len() {
                let instruction = cpu.program[cpu.program_counter];
                cpu.program_counter = cpu.program_counter + 1;
                let maybe_instruction = match instruction {
                    0 => adv(&mut cpu),
                    1 => bxl(&mut cpu),
                    2 => bst(&mut cpu),
                    3 => jnz(&mut cpu),
                    4 => bxc(&mut cpu),
                    5 => out(&mut cpu),
                    6 => bdv(&mut cpu),
                    7 => cdv(&mut cpu),
                    _ => panic!()
                };
                if maybe_instruction.is_some() {
                    new_program.push(maybe_instruction.unwrap());
                }
            }
            if new_program == self.data.program {
                break;
            }
            if new_program.len() > cpu.program.len() {
                low_bits = (a_start % ((1 << shift) -1 )) + 1;
                a_start >>= shift;
            } else {
                if new_program.ends_with(&cpu.program[cpu.program.len() - new_program.len() as usize..]) {
                    a_start = (a_start + low_bits) << shift;
                    low_bits = 0;
                } else {
                    low_bits += 1;
                }
                while low_bits == (1 << shift) {
                    low_bits = (a_start % ((1 << shift) -1 )) + 1;
                    a_start >>= shift;
                }
            }
            if a_start == 0 && low_bits == 1 {
                shift += 1;
            }
        }
        a_start + low_bits
    }
}

impl Default for D17Solver {
    fn default() -> D17Solver {
        D17Solver {data : CPU { register_a: u64::default(), register_b: u64::default(), register_c: u64::default(), program: vec![], program_counter: usize::default() }}
    }
}

fn get_combo(cpu: &mut CPU) -> u64 {
    let combo = cpu.program[cpu.program_counter];
    cpu.program_counter = cpu.program_counter + 1;
    match combo {
        0 => 0,
        1 => 1,
        2 => 2,
        3 => 3,
        4 => cpu.register_a,
        5 => cpu.register_b,
        6 => cpu.register_c,
        _ => panic!()
    }
}

fn get_value(cpu: &mut CPU) -> u64 {
    let value = cpu.program[cpu.program_counter];
    cpu.program_counter = cpu.program_counter + 1;
    value
}

fn adv(cpu: &mut CPU) -> Option<u64> {
    let combo = 2_u64.pow(get_combo(cpu) as u32);
    let a = cpu.register_a;
    cpu.register_a = a / combo;
    None
}

fn bxl(cpu: &mut CPU) -> Option<u64> {
    let value = get_value(cpu);
    cpu.register_b = cpu.register_b ^ value;    
    None
}

fn bst(cpu: &mut CPU) -> Option<u64> {
    let combo = get_combo(cpu);
    cpu.register_b = combo % 8;
    None
}

fn jnz(cpu: &mut CPU) -> Option<u64> {
    let value = get_value(cpu);
    if cpu.register_a != 0 {
        cpu.program_counter = value as usize;
    }
    None
}

fn bxc(cpu: &mut CPU) -> Option<u64> {
    let _combo = get_combo(cpu);
    cpu.register_b = cpu.register_b ^ cpu.register_c;
    None
}

fn out(cpu: &mut CPU) -> Option<u64> {
    let combo = get_combo(cpu);
    Some(combo % 8)
}

fn bdv(cpu: &mut CPU) -> Option<u64> {
    let combo = 2_u64.pow(get_combo(cpu) as u32);
    let a = cpu.register_a;
    cpu.register_b = a / combo;
    None
}

fn cdv(cpu: &mut CPU) -> Option<u64> {
    let combo = 2_u64.pow(get_combo(cpu) as u32);
    let a = cpu.register_a;
    cpu.register_c = a / combo;
    None
}
