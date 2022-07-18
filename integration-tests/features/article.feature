Feature: Article management
    As a system administrator
    I want to manage articles
    So that patients can be informed about their condition

    Scenario: Static articles
        Then there are the expected UK articles
        And there are the expected US articles

    Scenario: New article is created
        Given a new article is created
        When all articles are retrieved
        Then the article can be seen in all articles
        And the article can be retrieved by its uuid
        And the article matches that previously created

    Scenario: Article can be retrieved by tag
        Given a new article is created
        Then the article can be retrieved by its tag
        And the article matches that previously created

    Scenario: Article update
        Given a new article is created
        When the article is updated
        Then the updated article is persisted

    Scenario: Article delete
        Given a new article is created
        When the article is deleted
        And all articles are retrieved
        Then the article can not be seen in all articles
        And the article can not be retrieved by its uuid

    Scenario: Article fetch using ETag
        Given a new article is created
        And a new article is created
        And a new article is created
        When all articles are retrieved
