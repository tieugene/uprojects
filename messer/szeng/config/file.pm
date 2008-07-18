package szeng::config::file;

use strict;
use szeng::Object;

use vars qw($VERSION @ISA);
@ISA     	= qw(szeng::Object);

$VERSION = "0.0.1";

use Data::Dumper::Simple;
use Log::Log4perl;
use Config::Auto;

# ------------------------------------------------------------------------------------------------------------------------------
sub new {
    my $log = Log::Log4perl->get_logger("szeng::config::file");
    $log->trace("Создание объекта CONFIG::FILE");
    my $self  = shift;
    my $obj = bless{};
    $obj->outer;
}
# ------------------------------------------------------------------------------------------------------------------------------
sub getConfig{
    my $self  = shift;
    my $confFile = shift;
    my $log = Log::Log4perl->get_logger("szeng::config::file");
    $log->trace("Вызов метода getConfig");
    my $data = Config::Auto::parse($confFile);
    %$data;
}
# ------------------------------------------------------------------------------------------------------------------------------
1;
