#include <argp.h>
#include <stdbool.h>
#include <inttypes.h>
#include <float.h>

const char *argp_program_version = "Version: $major_version.$minor_version";
const char *argp_program_bug_address = "Chum Bucket customer service";
static char doc[] = "Perform a super secret operation.";
static char args_doc[] = "ARG1";
static struct argp_option options[] = {
    {"verbose",  'v', 0,      0,  "Produce verbose output" },
    {"quiet",    'q', 0,      0,  "Don't produce any output" },
    {"silent",   's', 0,      0,  "Just silence, no secrets" },
    { 0 } 
};

struct arguments {
    char *args[1];                /* arg1 */
    int silent, verbose;
};

static error_t parse_opt(int key, char *arg, struct argp_state *state) {
    struct arguments *arguments = state->input;
    switch (key) {
    case 'q': case 's':
        arguments->silent = 1;
        break;
    case 'v':
        arguments->verbose = 1;
        break;
    case ARGP_KEY_ARG: 
        if (state->arg_num >= 1)
            /* Too many arguments. */
            argp_usage (state);
        arguments->args[state->arg_num] = arg;
      break;
    case ARGP_KEY_END:
        if (state->arg_num < 1)
            /* Not enough arguments. */
            argp_usage (state);
        break;
    default: 
        return ARGP_ERR_UNKNOWN;
    }   
    return 0;
}

static struct argp argp = { options, parse_opt, args_doc, doc };

// Assumes little endian
void print_bits(size_t const size, void const * const ptr)
{
    unsigned char *b = (unsigned char*) ptr;
    unsigned char byte;
    int i, j;
    
    for (i = size-1; i >= 0; i--) {
        for (j = 7; j >= 0; j--) {
            byte = (b[i] >> j) & 1;
            printf("%u", byte);
        }
        printf(" ");
    }
    puts("");
}

int main(int argc, char **argv)
{
    struct arguments arguments;

    /* Default values */
    arguments.silent = 0;
    arguments.verbose = 0;

    argp_parse(&argp, argc, argv, 0, 0, &arguments);

    /* parse the argument */
    $operand_type num;
    sscanf(arguments.args[0], "$operand_fmt", &num);

    if (arguments.silent) {
        if (num == $secret_key) {
            printf("$secret\n");
        }
        else {
            printf("...\n");
        }
    }

    if (!arguments.silent) {
        $body
        if (arguments.verbose) {
            print_bits(sizeof(result), &result);
        }
    }

    return 0;
}
