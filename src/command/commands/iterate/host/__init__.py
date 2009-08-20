# $Id: __init__.py,v 1.2 2009/08/20 17:16:17 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.2  2009/08/20 17:16:17  bruno
# fix help
#
# Revision 1.1  2009/06/10 17:40:26  mjk
# - new verb interate
# - every object should have an iterate (right now just host)
# - '%' wildcard stuff should go into pylib
#

import os
import rocks.commands

class command(rocks.commands.HostArgumentProcessor,
	rocks.commands.iterate.command):
	pass

	
class Command(command):
	"""
	Iterate sequentially over a list of hosts.  This is used to run 
	a shell command on the frontend with with '%' wildcard expansion for
	every host specified.
				
        <arg optional='1' type='string' name='host' repeat='1'>
        Zero, one or more host names. If no host names are supplied iterate over
	all hosts except the frontend.
        </arg>

        <arg optional='1' type='string' name='command'>
	The shell command to be run for each host.  The '%' character is used as
	a wildcard to indicate the hostname.  Quoting of the '%' to expand to a 
	literal is accomplished with '%%'.
        </arg>
	
        <param type='string' name='command'>
        Can be used in place of the command argument.
        </param>

	<example cmd='iterate host compute "scp file %:/tmp/"'>
	Copies file to the /tmp directory of every compute node
	</example>

	<example cmd='iterate host compute command="scp file %:/tmp/"'>
	Same as above
	</example>
	"""

	def run(self, params, args):

		self.beginOutput()

		(args, cmd) = self.fillPositionalArgs(('command',))
		if not cmd:
			self.abort('requires a command')

		for host in self.getHostnames(args):

			# Turn the wildcard '%' into the hostname, and '%%' into
			# a single '%'.

			s = ''
			prev = ''
			for i in range(0, len(cmd)):
				curr = cmd[i]
				try:
					next = cmd[i+1]
				except:
					next = ''
				if curr == '%':
					if prev != '%' and next != '%':
						s   += host
						prev = host
						continue # consume '%'
					elif prev == '%':
						s   += '%'
						prev = '*'
						continue # consume '%'
				else:
					s += curr
				prev = curr

			for line in os.popen(s).readlines():
				self.addOutput(host, line[:-1])

		self.endOutput(padChar='')
