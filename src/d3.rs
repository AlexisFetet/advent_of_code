use std::fs;

#[derive(Debug)]
pub struct D3Solver {
    pub data: i32,
}

impl D3Solver {
    pub fn extract_info(&mut self, input: String) {
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");
    }

    pub fn solve_p1(&self) -> u32 {
        0
    }

    pub fn solve_p2(&self) -> u32 {
        0
    }
}

impl Default for D3Solver {
    fn default() -> D3Solver {
        D3Solver {data : 0}
    }
}