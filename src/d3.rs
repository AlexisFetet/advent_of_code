use std::fs;

use regex::Regex;

#[derive(Debug)]
pub struct D3Solver {
    pub data: Vec<(i32, i32, i32)>,
}

impl D3Solver {
    pub fn extract_info_p1(&mut self, input: String) {
        let re: Regex = Regex::new(r"\s*(?<num1>\d+)\s*(?<num2>\d+)\s*(?<num3>\d+)").unwrap();

        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        let instructions: Vec<(i32, i32, i32)> = re.captures_iter(&contents.as_str()).map(|captures| {
            let num1: &str = captures.name("num1").unwrap().as_str();
            let num1: i32 = num1.to_string().parse().unwrap();
            let num2: &str = captures.name("num2").unwrap().as_str();
            let num2: i32 = num2.to_string().parse().unwrap();
            let num3: &str = captures.name("num3").unwrap().as_str();
            let num3: i32 = num3.to_string().parse().unwrap();
            let mut temp = [num1, num2, num3];
            temp.sort();
            (temp[0], temp[1], temp[2])
        }).collect();

        self.data = instructions;
    }

    pub fn extract_info_p2(&mut self, input: String) {
        let re: Regex = Regex::new(r"\s*(?<num1>\d+)\s*(?<num2>\d+)\s*(?<num3>\d+)\n\s*(?<num4>\d+)\s*(?<num5>\d+)\s*(?<num6>\d+)\n\s*(?<num7>\d+)\s*(?<num8>\d+)\s*(?<num9>\d+)\n?").unwrap();

        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        let instructions = re.captures_iter(&contents.as_str()).map(|captures| {
            let num1: &str = captures.name("num1").unwrap().as_str();
            let num1: i32 = num1.to_string().parse().unwrap();
            let num2: &str = captures.name("num2").unwrap().as_str();
            let num2: i32 = num2.to_string().parse().unwrap();
            let num3: &str = captures.name("num3").unwrap().as_str();
            let num3: i32 = num3.to_string().parse().unwrap();
            let num4: &str = captures.name("num4").unwrap().as_str();
            let num4: i32 = num4.to_string().parse().unwrap();
            let num5: &str = captures.name("num5").unwrap().as_str();
            let num5: i32 = num5.to_string().parse().unwrap();
            let num6: &str = captures.name("num6").unwrap().as_str();
            let num6: i32 = num6.to_string().parse().unwrap();
            let num7: &str = captures.name("num7").unwrap().as_str();
            let num7: i32 = num7.to_string().parse().unwrap();
            let num8: &str = captures.name("num8").unwrap().as_str();
            let num8: i32 = num8.to_string().parse().unwrap();
            let num9: &str = captures.name("num9").unwrap().as_str();
            let num9: i32 = num9.to_string().parse().unwrap();
            let mut temp1 = [num1, num4, num7];
            let mut temp2 = [num2, num5, num8];
            let mut temp3 = [num3, num6, num9];
            temp1.sort();
            temp2.sort();
            temp3.sort();
            [(temp1[0], temp1[1], temp1[2]), (temp2[0], temp2[1], temp2[2]), (temp3[0], temp3[1], temp3[2])]
        });

        self.data.clear();
        for triplet in instructions {
            self.data.push(triplet[0]);
            self.data.push(triplet[1]);
            self.data.push(triplet[2]);
        }
    }

    pub fn solve(&self) -> u32 {
        let mut count = 0;

        for (num1, num2, num3) in self.data.iter() {
            if num1 + num2 > *num3 {
                count += 1;
            }
        }

        count
    }
}

impl Default for D3Solver {
    fn default() -> D3Solver {
        D3Solver {data : vec![]}
    }
}