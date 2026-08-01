from tmmp_integrations_mattermost.attachments import InteractiveAttachmentBuilder


def test_interactive_attachment_builder():
    attachment = (
        InteractiveAttachmentBuilder()
        .title("System Alert", link="https://status.example.com")
        .text("CPU usage exceeded 90%")
        .color("#FF0000")
        .add_field("Host", "web-server-01", short=True)
        .add_button("btn_acknowledge", "Acknowledge", "http://api.example.com/ack")
        .build()
    )

    assert attachment["title"] == "System Alert"
    assert attachment["color"] == "#FF0000"
    assert len(attachment["fields"]) == 1
    assert attachment["fields"][0]["title"] == "Host"
    assert len(attachment["actions"]) == 1
    assert attachment["actions"][0]["id"] == "btn_acknowledge"
