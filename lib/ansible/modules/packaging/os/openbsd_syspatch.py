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
            - C(absent) will revert all patches
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
stdout:
    description: stdout from syspatch(8)
stderr:
    description: stderr from syspatch(8)
'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        state=dict(type='str', required=True, default='latest'),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        stdout='',
        stdin=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
