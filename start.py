from src.app import create_app

if __name__ == '__main__':
    app = create_app()
    create_app().run(debug=False, port=7890)

    #TODO: TODO in remove_editor implement transfering of issues to another editor (done, but have to check whole implementation(must change editor id and editor of the issue that has been transfered)),
    #TODO: in subscriberNS
    #TODO: change model of Editor(add displaying of newspapers)
    #TODO: jsonify all of the returns
    #TODO: TESTS!!!