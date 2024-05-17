import streamlit as st
from collections import defaultdict, deque

# Function to find all possible transformations of a word
def get_neighbors(word, wordList):
    neighbors = []
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            neighbor = word[:i] + c + word[i+1:]
            if neighbor != word and neighbor in wordList:
                neighbors.append(neighbor)
    return neighbors

# Function to find the shortest path between two words
def word_ladder(beginWord, endWord, wordList):
    if endWord not in wordList:
        return []

    # Create a dictionary to store all possible transformations of a word
    word_dict = defaultdict(list)
    for word in wordList:
        for i in range(len(word)):
            pattern = word[:i] + '*' + word[i+1:]
            word_dict[pattern].append(word)

    # Perform breadth-first search to find the shortest path
    queue = deque([(beginWord, [beginWord])])
    visited = set([beginWord])
    while queue:
        word, path = queue.popleft()
        if word == endWord:
            return path
        for i in range(len(word)):
            pattern = word[:i] + '*' + word[i+1:]
            for next_word in word_dict[pattern]:
                if next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, path + [next_word]))
    return []

# Streamlit application
def main():
    st.title("Word Ladder Game")
    st.write("Transform the `beginWord` into the `endWord` by changing one letter at a time.")

    levels = [
        {"beginWord": "hit", "endWord": "cog", "wordList": "hot\ndot\ndog\nlot\nlog\ncog"},
        {"beginWord": "lead", "endWord": "gold", "wordList": "load\ngoad\ngold\ngeld\nglad"},
        {"beginWord": "cold", "endWord": "warm", "wordList": "cord\nward\ncard\nward\nwarm"}
    ]

    if 'level' not in st.session_state:
        st.session_state.level = 0
        st.session_state.total_points = 0

    if st.session_state.level < len(levels):
        current_level = levels[st.session_state.level]
        beginWord = current_level["beginWord"]
        endWord = current_level["endWord"]
        wordList = current_level["wordList"].split()
        
        st.write(f"Level {st.session_state.level + 1}")
        st.write(f"Start Word: {beginWord}")
        st.write(f"End Word: {endWord}")

        if st.button("Start Level"):
            st.session_state.current_word = beginWord
            st.session_state.steps = 0
            st.session_state.hints_used = 0
            st.session_state.wordList = wordList
            st.session_state.endWord = endWord
            st.session_state.max_points = 100  # Starting points
            st.session_state.current_points = st.session_state.max_points
            st.session_state.hint_shown = False

    if 'current_word' in st.session_state:
        st.write(f"Current word: {st.session_state.current_word}")
        guess = st.text_input("Enter your guess:").strip().lower()
        
        if st.button("Submit Guess"):
            if guess == st.session_state.endWord:
                st.write("Congratulations! You've reached the end word.")
                st.write(f"Total steps taken: {st.session_state.steps}")
                st.write(f"Points for this level: {st.session_state.current_points}")
                st.session_state.total_points += st.session_state.current_points
                st.session_state.level += 1
                del st.session_state.current_word
                if st.session_state.level < len(levels):
                    if st.button("Next Level"):
                        st.experimental_rerun()
            elif guess not in st.session_state.wordList:
                st.write("Invalid word. Please try again.")
            else:
                neighbors = get_neighbors(st.session_state.current_word, st.session_state.wordList)
                if guess not in neighbors:
                    st.write("Your guess must be a valid transformation. Please try again.")
                else:
                    st.session_state.current_word = guess
                    st.session_state.steps += 1
                    st.session_state.current_points -= 1  # Deduct points for each step
                    st.write(f"Current word updated to: {st.session_state.current_word}")

        if st.button("Get Hint"):
            if not st.session_state.hint_shown:
                st.session_state.hints_used += 1
                st.session_state.current_points -= 5  # Deduct points for each hint
                st.session_state.hint_shown = True
                st.write(f"Hint: The next possible word could be one of these - {get_neighbors(st.session_state.current_word, st.session_state.wordList)}")
            else:
                st.write("Hint has already been used.")
    
    if st.session_state.level >= len(levels):
        average_points = st.session_state.total_points / len(levels)
        st.write("Congratulations! You have completed all levels.")
        st.write(f"Total points: {st.session_state.total_points}")
        st.write(f"Average points per level: {average_points:.2f}")

if __name__ == "__main__":
    main()
