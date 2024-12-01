use crate::d1::D1Solver;

pub mod d1;

fn main() {

    // ----------------------------------------------

    let mut d1_solver: D1Solver = D1Solver{..Default::default()};

    d1_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d1/test/1.txt"));
    println!("Day1 test1 p1: {}", d1_solver.solve_p1());
    println!("Day1 test1 p2: {}", d1_solver.solve_p2());


    d1_solver.extract_info(String::from("/home/alexis/advent_of_code/data/d1/input.txt"));
    println!("Day1 p1: {}", d1_solver.solve_p1());
    println!("Day1 p2: {}", d1_solver.solve_p2());
}
