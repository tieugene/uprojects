//teststlset.cpp
// compile: g++ -o teststlset teststlset.cpp

#include <fstream>
#include <iostream>
#include <iterator>
#include <set>
#include <string>

int main(void) {
	std::set<std::string> a;
	a.insert("a");
	a.insert("c");
	a.insert("b");
	a.insert("b");
	std::set<std::string>::iterator i;
	for(i = a.begin(); i != a.end(); i++)
		std::cout << *i << std::endl;
}
