// use crate::d1::D1Solver;
// use crate::d2::D2Solver;
// use crate::d3::D3Solver;
// use crate::d4::D4Solver;
// use crate::d5::D5Solver;
// use crate::d6::D6Solver;
use crate::d7::D7Solver;

pub mod d1;
pub mod d2;
pub mod d3;
pub mod d4;
pub mod d5;
pub mod d6;
pub mod d7;

fn main() {

    // ----------------------------------------------

    // let mut d1_solver: D1Solver = D1Solver{..Default::default()};

    // d1_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d1/test/1.txt"));
    // println!("Day1 test1 p1: {}", d1_solver.solve_p1());


    // d1_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d1/test/2.txt"));
    // println!("Day1 test2 p1: {}", d1_solver.solve_p1());


    // d1_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d1/test/3.txt"));
    // println!("Day1 test3 p1: {}", d1_solver.solve_p1());


    // d1_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d1/test/4.txt"));
    // println!("Day1 test4 p2: {}", d1_solver.solve_p2());


    // d1_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d1/input.txt"));
    // println!("Day1 p1: {}", d1_solver.solve_p1());
    // println!("Day1 p2: {}", d1_solver.solve_p2());

    // ----------------------------------------------

    // let mut d2_solver: D2Solver = D2Solver{..Default::default()};
    // d2_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d2/test/1.txt"));
    // println!("Day2 test1 p1: {}", d2_solver.solve_p1());
    // println!("Day2 test1 p2: {}", d2_solver.solve_p2());

    // d2_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d2/input.txt"));
    // println!("Day2 p1: {}", d2_solver.solve_p1());
    // println!("Day2 p2: {}", d2_solver.solve_p2());

    // ----------------------------------------------

    // let mut d3_solver: D3Solver = D3Solver{..Default::default()};
    // d3_solver.extract_info_p1(String::from("/home/alexis/advent_of_code/data/d3/test/1.txt"));
    // println!("Day3 test1 p1: {}", d3_solver.solve());

    // d3_solver.extract_info_p2(String::from("/home/alexis/advent_of_code/data/d3/test/2.txt"));
    // println!("Day3 test2 p2: {}", d3_solver.solve());

    // d3_solver.extract_info_p1(String::from("/home/alexis/advent_of_code/data/d3/input.txt"));
    // println!("Day3 p1: {}", d3_solver.solve());

    // d3_solver.extract_info_p2(String::from("/home/alexis/advent_of_code/data/d3/input.txt"));
    // println!("Day3 p1: {}", d3_solver.solve());

    // ----------------------------------------------

    // let mut d4_solver: D4Solver = D4Solver{..Default::default()};
    // d4_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d4/test/1.txt"));
    // println!("Day4 test1 p1: {}", d4_solver.solve_p1());

    // d4_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d4/input.txt"));
    // println!("Day4 p1: {}", d4_solver.solve_p1());
    // println!("Day4 p2: {}", d4_solver.solve_p2());

    // ----------------------------------------------

    // let mut d5_solver: D5Solver = D5Solver{..Default::default()};
    // d5_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d5/test/1.txt"));
    // println!("Day5 test1 p1: {}", d5_solver.solve_p1());
    // println!("Day5 test1 p2: {}", d5_solver.solve_p2());

    // d5_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d5/input.txt"));
    // println!("Day5 p1: {}", d5_solver.solve_p1());
    // println!("Day5 p2: {}", d5_solver.solve_p2());

    // ----------------------------------------------

    // let mut d6_solver: D6Solver = D6Solver{..Default::default()};
    // d6_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d6/test/1.txt"));
    // println!("Day6 test1 p1: {}", d6_solver.solve_p1());
    // println!("Day6 test1 p2: {}", d6_solver.solve_p2());

    // d6_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d6/input.txt"));
    // println!("Day6 p1: {}", d6_solver.solve_p1());
    // println!("Day6 p2: {}", d6_solver.solve_p2());

    // ----------------------------------------------

    let mut d7_solver: D7Solver = D7Solver{..Default::default()};
    d7_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d7/test/1.txt"));
    println!("Day7 test1 p1: {}", d7_solver.solve_p1());

    d7_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d7/test/2.txt"));
    println!("Day7 test1 p2: {}", d7_solver.solve_p2());

    d7_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d7/input.txt"));
    println!("Day7 p1: {}", d7_solver.solve_p1());
    println!("Day7 p2: {}", d7_solver.solve_p2());

}
