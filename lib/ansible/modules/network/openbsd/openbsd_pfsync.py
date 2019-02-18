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
    name:
        description
            - Specify the name of the interface.
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
        name: pfsync0
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
        module.fail_json(
                msg='Failed to run command `{command}`: {err!r}'.format(
                    command=' '.join(cmd), err=err))
    return {'cmd': cmd, 'rc': rc, 'out': out, 'err': err}


def _create_pfsync_config(module)
   intf_str = 'inet' #FIXME
return inf_str


def save_pfsync_config(module):
    pfsync_config = _create_pfsync_config(module)
    with open('/etc/hostname.{}'.format(module.params.get('pfsync')), 'w') as f:
        f.write(pfsync_config)


def restart_interface(module):
    run_command(['netstart', module.params.get('pfsync')])


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        syncdev=dict(type='str', required=False),
        defer=dict(type='bool', default=False),
        maxudp:dict(type='int', default=False),
        syncpeer:dict(type='str', default=False),
    )

    result = dict(
        changed=False
        msg=[],
    )

    module = AnsibleModule(
        argument_spec=module_args,
        #supports_check_mode=True
    )

    if module.check_mode:
        #FIXME
        pass

    module.exit_json(**result)



def main():
    run_module()


if __name__ == '__main__':
    main()
