# -*- coding: utf-8 -*-
import logging
import salt.utils.yaml

log = logging.getLogger(__name__)


def ext_pillar(id,
               pillar,
               target_minions=[],
               pillar_path=None,
               key='ext'):

    if type(target_minions != list):
        target_minions = list(target_minions)

    match_found = False
    for pattern in target_minions:
        match_found = __salt__['match.compound'](pattern)
        if match_found:
            break

    syndic_pillar = {}
    if match_found:
        log.debug('minion %s gets data for %s', id, target_minions)

        if not pillar_path:
            # Get all pillar values for the minion running locally
            command = 'salt-call pillar.items --out=yaml'
        else:
            command = 'salt-call pillar.get {} --out=yaml'.format(pillar_path)

        # Run the cmd, capture the output
        output = __salt__['cmd.run_stdout'](command, python_shell=True)

        # load it as yaml, step down one level to remove the "local" keyword
        syndic_pillar[key] = salt.utils.yaml.safe_load(output)['local']

    log.debug('syndic_pillar %s', syndic_pillar)
    return syndic_pillar
