import random
import json
import os
import sys

SET_FILE = 'selected_set.txt'
SET_FOLDER = 'sets'

def get_sets():
    if not os.path.exists(SET_FOLDER):
        os.makedirs(SET_FOLDER)
    return [f for f in os.listdir(SET_FOLDER) if f.endswith('.json')]

def select_set():
    sets = get_sets()
    if not sets:
        print('No sets found. Create one with "newset".')
        return None
    print('Available sets:')
    for idx, s in enumerate(sets):
        print(f'{idx+1}: {s}')
    while True:
        choice = input('Select a set by number: ')
        if not choice.isdigit() or not (1 <= int(choice) <= len(sets)):
            print('Invalid choice.')
        else:
            selected = sets[int(choice)-1]
            with open(SET_FILE, 'w', encoding='utf-8') as f:
                f.write(selected)
            print(f'Selected set: {selected}')
            return selected

def get_selected_set():
    if not os.path.exists(SET_FILE):
        return None
    with open(SET_FILE, 'r', encoding='utf-8') as f:
        selected = f.read().strip()
    if not selected:
        return None
    return os.path.join(SET_FOLDER, selected)

def load_flashcards():
    selected = get_selected_set()
    if not selected or not os.path.exists(selected):
        return []
    with open(selected, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_flashcards(cards):
    selected = get_selected_set()
    if not selected:
        print('No set selected.')
        return
    with open(selected, 'w', encoding='utf-8') as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

def create_new_set():
    name = input('Enter a name for the new set: ').strip()
    if not name.endswith('.json'):
        name += '.json'
    if not os.path.exists(SET_FOLDER):
        os.makedirs(SET_FOLDER)
    set_path = os.path.join(SET_FOLDER, name)
    if os.path.exists(set_path):
        print('Set already exists.')
        return
    with open(set_path, 'w', encoding='utf-8') as f:
        json.dump([], f)
    with open(SET_FILE, 'w', encoding='utf-8') as f:
        f.write(name)
    print(f'Created and selected set: {name}')

def ascii_card(front, back=None, flipped=False):
    import textwrap
    width = 40
    border = '+' + '-' * (width - 2) + '+'
    if not flipped:
        text = front
        lines = textwrap.wrap(text, width=width - 4)
    else:
        if isinstance(back, list):
            lines = []
            for bline in back:
                lines.extend(textwrap.wrap(bline, width=width - 4))
                lines.append('')  # Add a blank line between back lines
        else:
            lines = textwrap.wrap(back if back else '', width=width - 4)
    content = '\n'.join(f'| {line.ljust(width - 4)} |' for line in lines)
    return f'{border}\n{content}\n{border}'

def create_flashcard():
    if not get_selected_set():
        print('No set selected. Use "select" or "newset".')
        return
    front = input('Enter the front of the card: ')
    print('Enter the back of the card (multiple lines, finish with TWO blank lines):')
    back_lines = []
    blank_count = 0
    while True:
        line = input()
        if line == '':
            blank_count += 1
        else:
            blank_count = 0
            back_lines.append(line)
        if blank_count == 2:
            break
    cards = load_flashcards()
    cards.append({'front': front, 'back': back_lines})
    save_flashcards(cards)
    print('Flashcard created!')

def show_random_flashcard():
    if not get_selected_set():
        print('No set selected. Use "select" or "newset".')
        return
    cards = load_flashcards()
    if not cards:
        print('No flashcards found.')
        return
    card = random.choice(cards)
    print(ascii_card(card['front'], card['back'], flipped=False))
    print('Use the "flip" command to see the back.')
    # Save last shown card for flipping
    with open('last_card.json', 'w', encoding='utf-8') as f:
        json.dump(card, f)

def flip_flashcard():
    if not get_selected_set():
        print('No set selected. Use "select" or "newset".')
        return
    if not os.path.exists('last_card.json'):
        print('No card to flip. Use "show" first.')
        return
    with open('last_card.json', 'r', encoding='utf-8') as f:
        card = json.load(f)
    print(ascii_card(card['front'], card['back'], flipped=True))

def autogenerate_set():
    # Usage: autogenerate <output_name> [--model <name>]
    args = sys.argv[2:]
    if len(args) < 1:
        print('Usage: python main.py autogenerate <output_name> [--model <name>]')
        return

    output_name = args[0]
    model = None

    i = 1
    while i < len(args):
        if args[i] == '--model' and i + 1 < len(args):
            model = args[i + 1]
            i += 2
        else:
            i += 1

    from autogenerate import autogenerate
    name = autogenerate(output_name, model=model)

    with open(SET_FILE, 'w', encoding='utf-8') as f:
        f.write(name)
    print(f'Selected set: {name}')


def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py [newset|select|create|show|flip|autogenerate|scrape]')
        return
    cmd = sys.argv[1]
    if cmd == 'newset':
        create_new_set()
    elif cmd == 'select':
        select_set()
    elif cmd == 'create':
        create_flashcard()
    elif cmd == 'show':
        show_random_flashcard()
    elif cmd == 'flip':
        flip_flashcard()
    elif cmd == 'autogenerate':
        autogenerate_set()
    elif cmd == 'scrape':
        from scrape_html import scrape
        scrape('web/page.html', 'web/page.txt')
    else:
        print('Unknown command.')
    
if __name__ == "__main__":
    main()