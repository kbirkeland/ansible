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
module: openbsd_carp

short_description: Manages carp(4) on OpenBSD

version_added: "2.7"

description:
    - "Manages carp(4) on OpenBSD"

options:
    carpnodes:
        description:
            - List of carpnode definitions
            - Valid keys are 'vhid', 'advbase', and 'advskew'
            - The key 'vhid' is required
        required: true
    carpdev:
        description:
            - Name of the carp interface
            - Must be in the format `carp<int>`
        required: true
    preempt:
        description:
            - Determines the preemption behavior
        default: false
    address:
        description:
            - Defines the VIP address
            - Must be in CIDR format (host/mask)
        required: true
    balancing:
        description:
            - C(none) does no balancing
            - C(ip) does IP based balancing
        default: none
    log:
        description:
            - Defines the logging level
            - Valid options are 0 - 7
        default: 2

author:
    - Kyle Birkeland (@kbirkeland)
    - Nicolas J. Bouliane (@nicboul)
'''

EXAMPLES = '''
FIXME
'''

RETURN = '''
msg:
    description: module message
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


def _create_carp_config(module)
    node_strs = []
    for node in module.params['carpnodes']:
        try:
            vhid = int(node.get('vhid'))
        except ValueError:
            module.fail_json(msg='Failed to convert vhid to integer (vhid={!r})'.format(node.get('vhid')))
        if vhid < 0 or vhid > 255:
            module.fail_json(msg='Invalid vhid {}'.format(vhid))

        advskew = node.get('advskew', 0)
        if advskew < 0 or advskew > 255:
            module.fail_json(msg='Invalid advskew {}'.format(advskew))

        node_strs.append('{}:{}'.format(vhid, advskew))
        
    node_str = ','.join(node_strs)

    # FIXME verify IP address
    
    intf_str = 'inet {address} carpnodes {carpnodes} carpdev {carpdev}'.format(
        module.params['address'],
        node_str,
        module.params['carpdev'])
    return intf_str


def save_carp_config(module):
    carp_config = _create_carp_config(module)
    with open('/etc/hostname.{}'.format(module.params.get('carpdev')), 'w') as f:
        f.write(carp_config)

def restart_interface(module):
    run_command(['netstart', module.params.get('carpdev')])

def run_module():
    module_args = dict(
        carpnodes=dict(type='list', required=True),
        carpdev=dict(type='str', required=True),
        preempt=dict(type='bool', default=False),
        address=dict(type='str', required=True),
        balancing=dict(type='str', default='none', choices=['none', 'ip']),
        log=dict(type='int', default=2, choices=list(range(8))),
    )

    result = dict(
        changed=False,
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
