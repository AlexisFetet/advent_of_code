use std::fs;

#[derive(Debug)]
pub struct DSolver {
    pub data: i32,
}

impl DSolver {
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

impl Default for DSolver {
    fn default() -> DSolver {
        DSolver {data : 0}
    }
}