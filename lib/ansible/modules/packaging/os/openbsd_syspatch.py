#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: openbsd_syspatch

short_description: Manages syspatch(8) on OpenBSD

version_added: "2.7"

description:
    - "Manages syspatch(8) on OpenBSD"

options:
    state:
        description:
            - C(latest) will update to the latest patch available
            - C(revert) will revert all patches
            - C(revert_all) will revert all patches
            - Default is C(latest)
        required: true

author:
    - Kyle Birkeland (@kbirkeland)
'''

EXAMPLES = '''
- name: Update to latest patch
  openbsd_syspatch:

- name: Revert all patches
  openbsd_syspatch:
    state: absent
'''

RETURN = '''
msg:
    description: module message
installed_patches:
    description: patches installed
reverted_patches:
    description: patches reverted
'''

from ansible.module_utils.basic import AnsibleModule

SYSPATCH_CMD = 'syspatch'

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
        module.fail_json(msg='Failed to run command `{command}`: {err!r}'.format(command=' '.join(cmd), err=err))
    return (rc, out, err)

def syspatch_installed(module):
    """Get list of installed patches"""
    cmd = [SYSPATCH_CMD, '-l']
    rc, out, err = run_command(module, cmd)
    return get_nonempty_lines(out)

def syspatch_available(module):
    cmd = [SYSPATCH_CMD, '-c']
    rc, out, err = run_command(module, cmd)
    return get_nonempty_lines(out)

def syspatch_latest(module):
    cmd = [SYSPATCH_CMD]
    rc, out, err = run_command(module, cmd)
    return

def syspatch_revert_last(module):
    cmd = [SYSPATCH_CMD, '-r']
    rc, out, err = run_command(module, cmd)
    return

def syspatch_revert_all(module):
    cmd = [SYSPATCH_CMD, '-R']
    rc, out, err = module.run_command(cmd)
    return

def run_module():
    module_args = dict(
        state=dict(type='str', required=True, choices=['latest', 'revert', 'revert_all']),
    )

    result = dict(
        changed=False,
        installed_patches=[],
        reverted_patches=[],
        msg=[],
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        if module.params['state'] == 'latest':
            result['available_patches'] = syspatch_available(module)
            result['installed_patches'] = available_patches
        elif module.params['state'] == 'revert_all':
            result['installed_patches'] = syspatch_installed(module)
            result['reverted_patches'] = installed_patches
        elif module.params['state'] == 'revert':
            result['installed_patches'] = syspatch_installed(module)
            result['reverted_patches'] = [installed_patches[-1]]
        else:
            module.fail_json(msg='unsupported state {}'.format(module.params['state']))
        return result

    if module.params['state'] == 'latest':
        available_patches = syspatch_available(module)
        if available_patches:
            syspatch_latest(module)
            result['changed'] = True
            result['installed_patches'] = available_patches
    elif module.params['state'] == 'revert_all':
        installed_patches = syspatch_installed(module)
        if installed_patches:
            syspatch_revert_all(module)
            result['changed'] = True
            result['reverted_patches'] = installed_patches
    elif module.params['state'] == 'revert':
        installed_patches = syspatch_installed(module)
        if installed_patches:
            syspatch_revert_last(module)
            result['changed'] = True
            result['reverted_patches'] = [installed_patches[-1]]
    else:
        module.fail_json(msg='unsupported state {}'.format(module.params['state']))

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
