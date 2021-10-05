# Jo
import gender_guesser.detector as gender
import re


def open_file(filename):
	return open(filename, 'r').read().split('\n')


def split_mail(email):
	return email.split('@')


def get_prefix(email):
	return split_mail(email)[0]


def get_domain(email):
	return split_mail(email)[1]


def remove_tld(domain):
	return domain.split('.')[0]


def get_sex(first):
	d = gender.Detector()
	return d.get_gender(u"{}".format(first))


def capitalize_list(arr):
	return list(map(str.capitalize, arr))


def remove_numbers(arr):
	return [''.join(x for x in i if x.isalpha()) for i in arr]


def trans_utf8(names):
	specials = {
		'Ae': 'Ä',
		'ae': 'ä',
		'Oe': 'Ö',
		'oe': 'ö',
		'Ue': 'Ü',
		'ue': 'ü',
		'ss': 'ß'
	}

	for s_orig in specials:
		s_utf8 = specials[s_orig]
		names = [name.replace(s_orig, s_utf8) for name in names]

	return names


def get_firstname(names):
	if len(names) >= 1:
		return names[0]
	return ''


def get_lastname(names):
	if len(names) >= 2:
		return names[1]
	return ''


def generate_sentence(first):
	sex = get_sex(first)
	if sex == 'male':
		return 'Sehr geehrter Herr '
	elif sex == 'female':
		return 'Sehr geehrte Frau '
	else:
		return 'Hallo '


def get_names(string):
	names = re.split('-|\.', string)
	names = capitalize_list(names)
	names = remove_numbers(names)
	names = trans_utf8(names)

	first = get_firstname(names)
	last = get_lastname(names)

	# Maybe switch names
	for name in names:
		if name in first_names:
			first = name
			names.remove(name)
			last = names[0]
			break

	sentence = generate_sentence(first)

	if len(first) < 2:
		first = ''

	if first:
		sentence += first
		sentence += ' '
	if last:
		sentence += last

	return {
		'first': first,
		'last': last,
		'sentence': sentence
	}


# Main
if __name__ == '__main__':

  examples = '\n'
  examples += 'johannes.mueller@gmail.com\n'
  examples += 'paypal@tim-zielzenzen.de\n'
  examples += 'maeyer.tim994@web.de\n'
  examples += 'ueberfigger.tim994@web.de\n'
  print('Beispiele: {}\n'.format(examples))

  while True:
    email = input('Schreib deine E-Mail hier: '.format(examples))
    prefix = get_prefix(email)
    domain = get_domain(email)
    providers = open_file('email-providers.txt')
    first_names = open_file('first-names.txt')

    if domain not in providers:
      # Domain doesnt exists in providers
      # Split the domain itself
      full_name = get_names(remove_tld(domain))
    else:
      # If Domain exists in Providers - split the Prefix
      full_name = get_names(prefix)

    print(full_name['sentence'])
