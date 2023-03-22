FROM quay.io/numigi/odoo-public:14.latest
MAINTAINER numigi <contact@numigi.com>

USER root

COPY .docker_files/requirements.txt .
RUN pip3 install -r requirements.txt

# Variable used for fetching private git repositories.
ARG GIT_TOKEN

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

USER odoo

COPY ./github_event /mnt/extra-addons/github_event
COPY ./github_event_webhook /mnt/extra-addons/github_event_webhook
COPY ./github_pull_request /mnt/extra-addons/github_pull_request
COPY ./github_pull_request_project /mnt/extra-addons/github_pull_request_project

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
