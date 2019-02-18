#!/usr/bin/python

# Copyright: (c) 2019, Kyle Birkeland <kylebirkeland@gmail.com>
# Copyright: (c) 2019, Nicolas J. Bouliane <nicboul@gmail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: pfsync

short_description: Manages pfsync(4) on OpenBSD

version_added: "2.7"

description:
    - "Manages pfsync(4) on OpenBSD"

options:
    syncdev:
        description:
            - Configure with a physical synchronisation interface,
            pfsync will also send state changes out on that interface.
    defer:
        description
            - Defer transmission of the initial packet of a connection
            the packet is queued until either this message is acknowledged
            by another system, or a timeout has expired.
    maxupd:
        description:
            - The maximum number of times a single state can be updated
            before a pfsync packet will be sent out.
    syncpeer:
        description:
            - An alternative destination address for pfsync packets can
            be specified using the syncpeer keyword.
author:
    - Kyle Birkeland (@kbirkeland)
    - Nicolas J. Bouliane (@nicboul)
'''

EXAMPLES = '''
- name: Manage pfsync(4) interface.
- pfsync:
        syncdev: fxp0
        defer: true
        maxupd: 100
        syncpeer: 192.168.1.50
'''

RETURN = '''
msg:
    description: module message
outputs:
    description: full command outputs
'''

def get_nonempty_lines(s):
    """Return a list of non-empty lines

    :arg s: string to split
    :returns: List of nonempty lines
    """
    return [line.strip() for line in s.split() if line]


def run_command(module, cmd):
    rc, out, err = module.run_command(cmd)
    module.log('ran {} got ({!r}, {!r}, {!r})'.format(cmd, rc, out, err))
    if rc != 0:
        if 'need root privileges' in err:
            module.fail_json(
                    msg='Failed to run command `{command}`: {err!r}'.format(
                        command=' '.join(cmd), err=err))
    return {'cmd': cmd, 'rc': rc, 'out': out, 'err': err}


def pfsync_up(module):
    """Get list of installed patches"""
    cmd = [SYSPATCH_CMD, '-l']
    output = run_command(module, cmd)
    return output, get_nonempty_lines(output['out'])

def run_module():
    module_args = dict(
        state=dict(
            type='str', required=True,
            choices=['latest', 'revert', 'revert_all']),
    )

    result = dict(
        changed=False,
        installed_patches=[],
        reverted_patches=[],
        msg=[],
        outputs=[],
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        if module.params['state'] == 'latest':
            output, available_patches = syspatch_available(module)
            result['outputs'].append(output)
            result['installed_patches'] = available_patches
        elif module.params['state'] == 'revert_all':
            output, installed_patches = syspatch_installed(module)
            result['outputs'].append(output)
            result['reverted_patches'] = installed_patches
        elif module.params['state'] == 'revert':
            output, installed_patches = syspatch_installed(module)
            result['outputs'].append(output)
            result['reverted_patches'] = [installed_patches[-1]]
        else:
            module.fail_json(
                msg='unsupported state {}'.format(module.params['state']))
        return result

    if module.params['state'] == 'latest':
        output, available_patches = syspatch_available(module)
        result['outputs'].append(output)
        if available_patches:
            output = syspatch_latest(module)
            result['outputs'].append(output)
            result['changed'] = True
            result['installed_patches'] = available_patches
    elif module.params['state'] == 'revert_all':
        output, installed_patches = syspatch_installed(module)
        result['outputs'].append(output)
        if installed_patches:
            output = syspatch_revert_all(module)
            result['outputs'].append(output)
            result['changed'] = True
            result['reverted_patches'] = installed_patches
    elif module.params['state'] == 'revert':
        output, installed_patches = syspatch_installed(module)
        result['outputs'].append(output)
        if installed_patches:
            output = syspatch_revert_last(module)
            result['outputs'].append(output)
            result['changed'] = True
            result['reverted_patches'] = [installed_patches[-1]]
    else:
        module.fail_json(
            msg='unsupported state {}'.format(module.params['state']))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
