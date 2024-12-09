use std::{fs, ops::Range};

use itertools::{min, Itertools};

#[derive(Debug)]
pub struct AoCFile {
    pub fid: u32,
    pub location: Vec<Range<u32>>,
}

#[derive(Debug)]
pub struct Storage {
    pub free_space: Vec<Range<u32>>,
    pub used_space: Vec<AoCFile>,
    pub size: u32
}

#[derive(Debug)]
pub struct D9Solver {
    pub internal_storage: Storage,
}

impl D9Solver {
    pub fn extract_info(&mut self, input: String) {
        let contents: String = fs::read_to_string(input)
            .expect("Should have been able to read the file");

        self.internal_storage.free_space.clear();
        self.internal_storage.used_space.clear();

        let mut next_fid = 0;
        let mut current_mem_block = 0;
        let mut is_file = true;

        for digit in contents.as_str().chars().map(| character | character.to_digit(10).unwrap()).collect_vec() {
            if is_file {
                self.internal_storage.used_space.push(AoCFile{fid: next_fid, location: vec![Range{start: current_mem_block, end: current_mem_block + digit}]});
                current_mem_block += digit;
                next_fid += 1;
            } else if digit != 0 {
                self.internal_storage.free_space.push(Range{start: current_mem_block, end: current_mem_block + digit});
                current_mem_block += digit;
            }
            is_file = !is_file;
        }
        self.internal_storage.size = self.internal_storage.used_space[self.internal_storage.used_space.len() - 1].location[0].end;
    }

    pub fn solve_p1(&self) -> u64 {
        let mut free_space = self.internal_storage.free_space.clone();
        let mut used_space = self.internal_storage.used_space.clone();
        let mut disk_size = self.internal_storage.size;
        while free_space.len() > 0 {
            let next_free_space = &free_space[0].clone();
            let (last_file_index, last_file) = used_space.iter().find_position(| aoc_file | aoc_file.location.iter().any(| used_range | used_range.end == disk_size)).unwrap();
            let last_file_size = last_file.location[0].len();
            let moved_blocks = match min([last_file.location[0].len(), next_free_space.len()]) {
                Some(min_value) => min_value, 
                None => last_file_size
            };
            // total freed space (add extra if all file is moved)
            let mut freed_space = moved_blocks as u32;
            // declare newly used space
            let used_range = Range {start: next_free_space.start, end: next_free_space.start + moved_blocks as u32};
            // reserve space
            if next_free_space.len() == moved_blocks {
                free_space.remove(0);
            } else {
                free_space[0] = Range{start: next_free_space.start + moved_blocks as u32, end: next_free_space.end};
            }
            // move
            if last_file.location[0].len() == moved_blocks {
                if free_space[free_space.len() - 1].end ==  last_file.location[0].start {
                    freed_space = freed_space + free_space[free_space.len() - 1].len() as u32;
                    free_space.remove(free_space.len() - 1); // we move the whole file so before it is free space
                }
                used_space[last_file_index].location.remove(0);            
            } else {
                used_space[last_file_index].location[0] = Range{start: last_file.location[0].start, end: last_file.location[0].end - moved_blocks as u32};
            }
            used_space[last_file_index].location.push(used_range);
            disk_size = disk_size - freed_space;
        }
        used_space.iter().fold(0, | acc, aoc_file | {
            acc + aoc_file.fid as u64 * aoc_file.location.iter().fold(0, | internal_acc, used_range | {
                internal_acc + (((used_range.end - 1) * used_range.end - (used_range.start - 1) * (used_range.start)) /2) as u64
            })
        })
    }

    pub fn solve_p2(&self) -> u64 {
        let mut free_space = self.internal_storage.free_space.clone();
        let mut used_space = self.internal_storage.used_space.clone();
        for aoc_file in used_space.iter_mut().rev() {
            // try to find an element with enough free space
            let first_free_space;
            let first_free_space_index;
            let candidate = free_space.iter().find_position(| free_space | free_space.len() >= aoc_file.location[0].len() && free_space.start < aoc_file.location[0].start);
            if candidate.is_none() {
                continue;
            } else {
                (first_free_space_index, first_free_space) = candidate.unwrap();
            }
            let used_range = Range {start: first_free_space.start, end: first_free_space.start + aoc_file.location[0].len() as u32};
            let freed_range = aoc_file.location[0].clone();
            // reserve space
            if first_free_space.len() == aoc_file.location[0].len() {
                free_space.remove(first_free_space_index);
            } else {
                free_space[first_free_space_index] = Range{start: first_free_space.start + aoc_file.location[0].len() as u32, end: first_free_space.end};
            }
            // update file location
            aoc_file.location[0] = used_range;
            // look for free space before
            let candidate_before = free_space.iter().find_position(| free_space | free_space.end == freed_range.start);
            // look for free space after
            let candidate_after = free_space.iter().find_position(| free_space | free_space.start == freed_range.end);
            // proceed to merge
            if candidate_before.is_some() && candidate_after.is_some() {
                let (before_index, before) = candidate_before.unwrap();
                let (after_index, after) = candidate_after.unwrap();
                free_space[before_index] = Range{start: before.start, end: after.end};
                free_space.remove(after_index);
            } else if candidate_before.is_some() && !candidate_after.is_some() {
                let (before_index, before) = candidate_before.unwrap();
                free_space[before_index] = Range{start: before.start, end: freed_range.end};
            } else if !candidate_before.is_some() && candidate_after.is_some() {
                let (after_index, after) = candidate_after.unwrap();
                free_space[after_index] = Range{start: freed_range.start, end: after.end};
            } else {
                free_space.push(freed_range);
            }
        }
        used_space.iter().fold(0, | acc, aoc_file | {
            acc + aoc_file.fid as u64 * aoc_file.location.iter().fold(0, | internal_acc, used_range | {
                internal_acc + (((used_range.end - 1) * used_range.end - (used_range.start - 1) * (used_range.start)) /2) as u64
            })
        })
    }
}

impl Clone for AoCFile {
    fn clone(&self) -> AoCFile {
        AoCFile {fid : self.fid, location: self.location.clone()}
    }
}

impl Default for Storage {
    fn default() -> Storage {
        Storage {free_space : vec![], used_space: vec![], size: 0}
    }
}

impl Default for D9Solver {
    fn default() -> D9Solver {
        D9Solver {internal_storage : Storage::default()}
    }
}