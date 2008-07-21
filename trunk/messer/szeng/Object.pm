package szeng::Object;
#----------------------------------------------------------------------
# Description:
# Author: SlavaZ 
# Created at: Mon Jul 21 16:23:16 EEST 2008
#    
# Copyright (c) 2008 SlavaZ  All rights reserved.
#
#----------------------------------------------------------------------
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer,
#    without modification.
# 2. Redistributions in binary form must reproduce at minimum a disclaimer
#    substantially similar to the "NO WARRANTY" disclaimer below
#    ("Disclaimer") and any redistribution must be conditioned upon
#    including a substantially similar Disclaimer requirement for further
#    binary redistribution.
# 3. Neither the names of the above-listed copyright holders nor the names
#    of any contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# Alternatively, this software may be distributed under the terms of the
# GNU General Public License ("GPL") version 2 as published by the Free
# Software Foundation.
#
# NO WARRANTY
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTIBILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDERS OR CONTRIBUTORS BE LIABLE FOR SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGES.
# 

require 5.005;

use strict;
use Tie::Hash;

use vars qw($VERSION @ISA);
@ISA     	= qw(Tie::StdHash);

$VERSION = "0.0.1";


# ------------------------------------------------------------------------------------------------------------------------------
sub Version { 
    $VERSION; 
}
# ------------------------------------------------------------------------------------------------------------------------------
sub outer {
  my $self = shift;
  return $self if tied(%$self);
  my %outer;
  tie %outer, ref($self), $self;
  ++$self->{net_ldap_refcnt};
  bless \%outer, ref($self);
}
# ------------------------------------------------------------------------------------------------------------------------------
sub inner {
  tied(%{$_[0]}) || $_[0];
}
# ------------------------------------------------------------------------------------------------------------------------------
sub TIEHASH {
  $_[1];
}
# ------------------------------------------------------------------------------------------------------------------------------
1;
