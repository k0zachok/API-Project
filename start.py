from src.app import create_app

if __name__ == '__main__':
    app = create_app()
    create_app().run(debug=False, port=7890)

    #TODO: Perfectly: remove_editor if there is no other editor - return an error
    #TODO: Perfectly:   in subscriberNS
    #TODO: Perfectly:   change model of Editor(add displaying of newspapers)
    #TODO: Add to tests in EditorNS check for the incorrect given ID
    #TODO: TODO: Implement 3 more tests(2 stats and missing issues)
